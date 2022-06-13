import lzma
import random
from collections import defaultdict
from dataclasses import dataclass
from os.path import join
from pathlib import Path
from typing import Any, Dict, List, Tuple

import msgpack
from bokeh.document.document import Document
from bokeh.io import show
from bokeh.layouts import column

from nuplan.common.actor_state.vehicle_parameters import get_pacifica_parameters
from nuplan.common.maps.nuplan_map.map_factory import NuPlanMapFactory
from nuplan.database.nuplan_db.nuplandb import NuPlanDB
from nuplan.database.nuplan_db.nuplandb_wrapper import NuPlanDBWrapper
from nuplan.planning.nuboard.base.data_class import NuBoardFile, SimulationScenarioKey
from nuplan.planning.nuboard.base.simulation_tile import SimulationTile
from nuplan.planning.scenario_builder.abstract_scenario import AbstractScenario
from nuplan.planning.scenario_builder.nuplan_db.nuplan_scenario import NuPlanScenario
from nuplan.planning.scenario_builder.nuplan_db.nuplan_scenario_utils import (
    DEFAULT_SCENARIO_NAME,
    ScenarioExtractionInfo,
)
from nuplan.planning.simulation.callback.serialization_callback import SceneColors, convert_sample_to_scene
from nuplan.planning.simulation.controller.perfect_tracking import PerfectTrackingController
from nuplan.planning.simulation.history.simulation_history import SimulationHistory, SimulationHistorySample
from nuplan.planning.simulation.history.simulation_history_buffer import SimulationHistoryBuffer
from nuplan.planning.simulation.observation.tracks_observation import TracksObservation
from nuplan.planning.simulation.simulation_time_controller.step_simulation_time_controller import (
    StepSimulationTimeController,
)
from nuplan.planning.simulation.trajectory.interpolated_trajectory import InterpolatedTrajectory


@dataclass
class HydraConfigPaths:
    """
    Stores relative hydra paths to declutter tutorial.
    """

    common_dir: str
    config_name: str
    config_path: str
    experiment_dir: str


def construct_nuboard_hydra_paths(base_config_path: str) -> HydraConfigPaths:
    """
    Specifies relative paths to nuBoard configs to pass to hydra to declutter tutorial.
    :param base_config_path: Base config path.
    :return Hydra config path.
    """
    common_dir = "file://" + join(base_config_path, 'config', 'common')
    config_name = 'default_nuboard'
    config_path = join(base_config_path, 'config/nuboard')
    experiment_dir = "file://" + join(base_config_path, 'experiments')
    return HydraConfigPaths(common_dir, config_name, config_path, experiment_dir)


def construct_simulation_hydra_paths(base_config_path: str) -> HydraConfigPaths:
    """
    Specifies relative paths to simulation configs to pass to hydra to declutter tutorial.
    :param base_config_path: Base config path.
    :return Hydra config path.
    """
    common_dir = "file://" + join(base_config_path, 'config', 'common')
    config_name = 'default_simulation'
    config_path = join(base_config_path, 'config', 'simulation')
    experiment_dir = "file://" + join(base_config_path, 'experiments')
    return HydraConfigPaths(common_dir, config_name, config_path, experiment_dir)


def save_scenes_to_dir(
    scenes: List[Dict[str, Any]], scenario: AbstractScenario, save_dir: str
) -> SimulationScenarioKey:
    """
    Save scenes to a directory.
    :param scenes: A list of scene dicts.
    :param scenario: Scenario.
    :param save_dir: Save path.
    :return Scenario key of simulation.
    """
    planner_name = "tutorial_planner"
    scenario_type = scenario.scenario_type
    scenario_name = scenario.scenario_name

    save_path = Path(save_dir)
    file = save_path / planner_name / scenario_type / scenario_name / (scenario_name + ".msgpack.xz")
    file.parent.mkdir(exist_ok=True, parents=True)

    with lzma.open(file, "wb", preset=0) as f:
        f.write(msgpack.packb(scenes))

    return SimulationScenarioKey(
        planner_name=planner_name, scenario_name=scenario_name, scenario_type=scenario_type, files=[file]
    )


def serialize_scenario(
    scenario: AbstractScenario, num_poses: int = 12, future_time_horizon: float = 6.0
) -> List[Dict[str, Any]]:
    """
    Serialize a scenario to a list of scene dicts.
    :param scenario: Scenario.
    :param num_poses: Number of poses in trajectory.
    :param future_time_horizon: Future time horizon in trajectory.
    :return A list of scene dicts.
    """
    simulation_history = SimulationHistory(scenario.map_api, scenario.get_mission_goal())
    ego_controller = PerfectTrackingController(scenario)
    simulation_time_controller = StepSimulationTimeController(scenario)
    observations = TracksObservation(scenario)

    # Dummy history buffer
    history_buffer = SimulationHistoryBuffer([], [])

    # Get all states
    for _ in range(simulation_time_controller.number_of_iterations()):
        iteration = simulation_time_controller.get_iteration()
        ego_state = ego_controller.get_state()
        observation = observations.get_observation()

        # Log play back trajectory
        current_state = scenario.get_ego_state_at_iteration(iteration.index)
        states = scenario.get_ego_future_trajectory(iteration.index, future_time_horizon, num_poses)
        trajectory = InterpolatedTrajectory([current_state] + states)

        simulation_history.add_sample(SimulationHistorySample(iteration, ego_state, trajectory, observation))
        next_iteration = simulation_time_controller.next_iteration()

        if next_iteration:
            ego_controller.update_state(iteration, next_iteration, ego_state, trajectory)
            observations.update_observation(iteration, next_iteration, history_buffer)

    # Serialize to file
    scenes = [
        convert_sample_to_scene(
            map_name=scenario.map_api.map_name,
            database_interval=scenario.database_interval,
            traffic_light_status=scenario.get_traffic_light_status_at_iteration(index),
            expert_trajectory=scenario.get_expert_ego_trajectory(),
            mission_goal=scenario.get_mission_goal(),
            data=sample,
            colors=SceneColors(),
        )
        for index, sample in enumerate(simulation_history.data)
    ]
    return scenes


def visualize_scenario(scenario: NuPlanScenario, save_dir: str = '/tmp/scenario_visualization/') -> None:
    """
    Visualize a scenario in Bokeh.
    :param scenario: Scenario object to be visualized.
    :param save_dir: Dir to save serialization and visualization artifacts.
    """
    map_factory = NuPlanMapFactory(scenario._db.maps_db)
    scenes = serialize_scenario(scenario)
    simulation_scenario_key = save_scenes_to_dir(scenes=scenes, scenario=scenario, save_dir=save_dir)
    visualize_scenarios([simulation_scenario_key], map_factory, Path(save_dir))


def visualize_scenarios(
    simulation_scenario_keys: List[SimulationScenarioKey], map_factory: NuPlanMapFactory, save_path: Path
) -> None:
    """
    Visualize scenarios in Bokeh.
    :param simulation_scenario_keys: A list of simulation scenario keys.
    :param map_factory: Map factory object to use for rendering.
    :param save_path: Path where to save the scene dict.
    """

    def bokeh_app(doc: Document) -> None:
        """Run bokeh app in jupyter notebook."""
        # Change simulation_main_path to a folder where you want to save rendered videos.
        nuboard_file = NuBoardFile(
            simulation_main_path=save_path.name,
            simulation_folder='',
            metric_main_path='',
            metric_folder='',
            aggregator_metric_folder='',
        )

        # Create a simulation tile
        simulation_tile = SimulationTile(
            doc=doc,
            map_factory=map_factory,
            nuboard_files=[nuboard_file],
            vehicle_parameters=get_pacifica_parameters(),
        )

        # Render a simulation tile
        layouts = simulation_tile.render_simulation_tiles(simulation_scenario_keys)

        # Create layouts
        layouts = column(layouts, width_policy='max', sizing_mode='scale_width')

        # Add the layouts to the bokeh document
        doc.add_root(layouts)

    show(bokeh_app)


def get_default_scenario_extraction(
    scenario_duration: float = 15.0,
    extraction_offset: float = -2.0,
    subsample_ratio: float = 0.5,
) -> ScenarioExtractionInfo:
    """
    Get default scenario extraction instructions used in visualization.
    :param scenario_duration: [s] Duration of scenario.
    :param extraction_offset: [s] Offset of scenario (e.g. -2 means start scenario 2s before it starts).
    :param subsample_ratio: Scenario resolution.
    :return: Scenario extraction info object.
    """
    return ScenarioExtractionInfo(DEFAULT_SCENARIO_NAME, scenario_duration, extraction_offset, subsample_ratio)


def get_default_scenario_from_token(log_db: NuPlanDB, token: str) -> NuPlanScenario:
    """
    Build a scenario with default parameters for visualization.
    :param log_db: Log database object that the token belongs to.
    :param token: Lidar pc token to be used as anchor for the scenario.
    :return: Instantiated scenario object.
    """
    args = [DEFAULT_SCENARIO_NAME, get_default_scenario_extraction(), get_pacifica_parameters()]
    return NuPlanScenario(log_db, log_db.log_name, token, *args)


def get_scenario_type_token_map(db: NuPlanDBWrapper) -> Dict[str, List[Tuple[NuPlanDB, str]]]:
    """Get a map from scenario types to lists of all instances for a given scenario type in the database."""
    available_scenario_types = defaultdict(list)
    for log_db in db.log_dbs:
        for tag in log_db.scenario_tag:
            available_scenario_types[tag.type].append((log_db, tag.lidar_pc_token))

    return available_scenario_types


def visualize_nuplan_scenarios(db: NuPlanDBWrapper) -> None:
    """Create a dropdown box populated with unique scenario types to visualize from a database."""
    from IPython.display import clear_output, display
    from ipywidgets import Dropdown, Output

    scenario_type_token_map = get_scenario_type_token_map(db)
    out = Output()
    drop_down = Dropdown(description='Scenario', options=sorted(scenario_type_token_map.keys()))

    def scenario_dropdown_handler(change: Any) -> None:
        """Dropdown handler that randomly chooses a scenario from the selected scenario type and renders it."""
        with out:
            clear_output()

            scenario_type = str(change.new)
            log_db, token = random.choice(scenario_type_token_map[scenario_type])
            scenario = get_default_scenario_from_token(log_db, token)
            visualize_scenario(scenario)

    display(drop_down)
    display(out)
    drop_down.observe(scenario_dropdown_handler, names='value')
