from __future__ import annotations

import logging
from functools import partial
from typing import Any, List, Optional, Tuple, Type, Union, cast

from nuplan.common.actor_state.vehicle_parameters import VehicleParameters, get_pacifica_parameters
from nuplan.common.maps.nuplan_map.map_factory import NuPlanMapFactory, get_maps_db
from nuplan.planning.scenario_builder.abstract_scenario import AbstractScenario
from nuplan.planning.scenario_builder.abstract_scenario_builder import AbstractScenarioBuilder
from nuplan.planning.scenario_builder.nuplan_db.nuplan_scenario import NuPlanScenario
from nuplan.planning.scenario_builder.nuplan_db.nuplan_scenario_filter_utils import (
    FilterWrapper,
    GetScenariosFromDbFileParams,
    ScenarioDict,
    discover_log_dbs,
    filter_num_scenarios_per_type,
    filter_total_num_scenarios,
    get_scenarios_from_log_file,
    scenario_dict_to_list,
)
from nuplan.planning.scenario_builder.nuplan_db.nuplan_scenario_utils import ScenarioMapping, absolute_path_to_log_name
from nuplan.planning.scenario_builder.scenario_filter import ScenarioFilter
from nuplan.planning.simulation.trajectory.trajectory_sampling import TrajectorySampling
from nuplan.planning.utils.multithreading.worker_utils import WorkerPool, worker_map

logger = logging.getLogger(__name__)


class NuPlanScenarioBuilder(AbstractScenarioBuilder):
    """Builder class for constructing nuPlan scenarios for training and simulation."""

    def __init__(
        self,
        data_root: str,
        map_root: str,
        db_files: Optional[Union[List[str], str]],
        map_version: str,
        max_workers: Optional[int] = None,
        verbose: bool = True,
        scenario_mapping: Optional[ScenarioMapping] = None,
        vehicle_parameters: Optional[VehicleParameters] = None,
        ground_truth_predictions: Optional[TrajectorySampling] = None,
    ):
        """
        Initialize scenario builder that filters and retrieves scenarios from the nuPlan dataset.
        :param data_root: Local data root for loading (or storing downloaded) the log databases.
                          If `db_files` is not None, all downloaded databases will be stored to this data root.
                          E.g.: /data/sets/nuplan
        :param map_root: Local map root for loading (or storing downloaded) the map database.
        :param db_files: Path to load the log database(s) from.
                         It can be a local/remote path to a single database, list of databases or dir of databases.
                         If None, all database filenames found under `data_root` will be used.
                         E.g.: /data/sets/nuplan-v1.0-mini/2021.10.11.08.31.07_veh-50_01750_01948.db
        :param map_version: Version of map database to load. The map database is passed to each loaded log database.
        :param max_workers: Maximum number of workers to use when loading the databases concurrently.
                            Only used when the number of databases to load is larger than this parameter.
        :param verbose: Whether to print progress and details during the database loading and scenario building.
        :param scenario_mapping: Mapping of scenario types to extraction information.
        :param vehicle_parameters: Vehicle parameters for this db.
        """
        self._data_root = data_root
        self._map_root = map_root
        self._db_files = discover_log_dbs(data_root if db_files is None else db_files)
        self._map_version = map_version
        self._max_workers = max_workers
        self._verbose = verbose
        self._ground_truth_predictions = ground_truth_predictions
        self._scenario_mapping = scenario_mapping if scenario_mapping is not None else ScenarioMapping({}, None)
        self._vehicle_parameters = vehicle_parameters if vehicle_parameters is not None else get_pacifica_parameters()

    def __reduce__(self) -> Tuple[Type[NuPlanScenarioBuilder], Tuple[Any, ...]]:
        """
        :return: tuple of class and its constructor parameters, this is used to pickle the class
        """
        return self.__class__, (
            self._data_root,
            self._map_root,
            self._db_files,
            self._map_version,
            self._max_workers,
            self._verbose,
            self._scenario_mapping,
            self._vehicle_parameters,
            self._ground_truth_predictions,
        )

    @classmethod
    def get_scenario_type(cls) -> Type[AbstractScenario]:
        """Inherited. See superclass."""
        return cast(Type[AbstractScenario], NuPlanScenario)

    def get_map_factory(self) -> NuPlanMapFactory:
        """Inherited. See superclass."""
        return NuPlanMapFactory(get_maps_db(self._map_root, self._map_version))

    def _aggregate_dicts(self, dicts: List[ScenarioDict]) -> ScenarioDict:
        """
        Combines multiple scenario dicts into a single dictionary by concatenating lists of matching scenario names.
        Sample input:
            [{"a": [1, 2, 3], "b": [2, 3, 4]}, {"b": [3, 4, 5], "c": [4, 5]}]
        Sample output:
            {"a": [1, 2, 3], "b": [2, 3, 4, 3, 4, 5], "c": [4, 5]}
        :param dicts: The list of dictionaries to concatenate.
        :return: The concatenated dictionaries.
        """
        output_dict = dicts[0]
        for merge_dict in dicts[1:]:
            for key in merge_dict:
                if key not in output_dict:
                    output_dict[key] = merge_dict[key]
                else:
                    output_dict[key] += merge_dict[key]

        return output_dict

    def _create_scenarios(self, scenario_filter: ScenarioFilter, worker: WorkerPool) -> ScenarioDict:
        """
        Creates a scenario dictionary with scenario type as key and list of scenarios for each type.
        :param scenario_filter: Structure that contains scenario filtering instructions.
        :param worker: Worker pool for concurrent scenario processing.
        :return: Constructed scenario dictionary.
        """
        allowable_log_names = set(scenario_filter.log_names) if scenario_filter.log_names is not None else None
        map_parameters = [
            GetScenariosFromDbFileParams(
                data_root=self._data_root,
                log_file_absolute_path=log_file,
                expand_scenarios=scenario_filter.expand_scenarios,
                map_root=self._map_root,
                map_version=self._map_version,
                scenario_mapping=self._scenario_mapping,
                vehicle_parameters=self._vehicle_parameters,
                ground_truth_predictions=self._ground_truth_predictions,
                filter_tokens=scenario_filter.scenario_tokens,
                filter_types=scenario_filter.scenario_types,
                filter_map_names=scenario_filter.map_names,
            )
            for log_file in self._db_files
            if (allowable_log_names is None) or (absolute_path_to_log_name(log_file) in allowable_log_names)
        ]

        if len(map_parameters) == 0:
            raise ValueError("No log files found! Make sure they are available in your environment.")

        dicts = worker_map(worker, get_scenarios_from_log_file, map_parameters)

        return self._aggregate_dicts(dicts)

    def _create_filter_wrappers(self, scenario_filter: ScenarioFilter, worker: WorkerPool) -> List[FilterWrapper]:
        """
        Creates a series of filter wrappers that will be applied sequentially to construct the list of scenarios.
        :param scenario_filter: Structure that contains scenario filtering instructions.
        :param worker: Worker pool for concurrent scenario processing.
        :return: Series of filter wrappers.
        """
        filters = [
            FilterWrapper(
                fn=partial(
                    filter_num_scenarios_per_type,
                    num_scenarios_per_type=scenario_filter.num_scenarios_per_type,
                    randomize=scenario_filter.shuffle,
                ),
                enable=(scenario_filter.num_scenarios_per_type is not None),
                name='num_scenarios_per_type',
            ),
            FilterWrapper(
                fn=partial(
                    filter_total_num_scenarios,
                    limit_total_scenarios=scenario_filter.limit_total_scenarios,
                    randomize=scenario_filter.shuffle,
                ),
                enable=(scenario_filter.limit_total_scenarios is not None),
                name='limit_total_scenarios',
            ),
        ]

        return filters

    def get_scenarios(self, scenario_filter: ScenarioFilter, worker: WorkerPool) -> List[AbstractScenario]:
        """Implemented. See interface."""
        # Create scenario dictionary and series of filters to apply
        scenario_dict = self._create_scenarios(scenario_filter, worker)
        filter_wrappers = self._create_filter_wrappers(scenario_filter, worker)

        # Apply filtering strategy sequentially to the scenario dictionary
        for filter_wrapper in filter_wrappers:
            scenario_dict = filter_wrapper.run(scenario_dict)

        return scenario_dict_to_list(scenario_dict, shuffle=scenario_filter.shuffle)  # type: ignore
