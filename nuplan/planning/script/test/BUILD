load("@rules_python//python:defs.bzl", "py_library", "py_test")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "skeleton_test_train",
    srcs = ["skeleton_test_train.py"],
    deps = [
        "//nuplan/planning/script:run_training",
    ],
)

py_library(
    name = "skeleton_test_simulation",
    srcs = ["skeleton_test_simulation.py"],
    deps = [
        "//nuplan/planning/scenario_builder/nuplan_db:nuplan_scenario_builder",
        "//nuplan/planning/scenario_builder/test:mock_abstract_scenario",
        "//nuplan/planning/script:run_simulation",
        "//nuplan/planning/script/builders:model_builder",
        "//nuplan/planning/script/builders:worker_pool_builder",
        "//nuplan/planning/simulation/controller:log_playback",
        "//nuplan/planning/simulation/observation:tracks_observation",
        "//nuplan/planning/simulation/planner:abstract_planner",
        "//nuplan/planning/simulation/planner:simple_planner",
        "//nuplan/planning/simulation/simulation_time_controller:step_simulation_time_controller",
        "//nuplan/planning/training/callbacks:profile_callback",
        "//nuplan/planning/training/modeling:lightning_module_wrapper",
    ],
)

py_test(
    name = "test_config_dataloader",
    size = "large",
    srcs = ["test_config_dataloader.py"],
    data = [
        "//nuplan/planning/script:yaml",
    ],
    deps = [
        "//nuplan/planning/scenario_builder/nuplan_db:nuplan_scenario_builder",
        "//nuplan/planning/script/builders:data_augmentation_builder",
        "//nuplan/planning/script/builders:model_builder",
        "//nuplan/planning/script/builders:scenario_building_builder",
        "//nuplan/planning/script/builders:training_builder",
        "//nuplan/planning/script/builders:training_callback_builder",
        "//nuplan/planning/script/builders:training_metrics_builder",
        "//nuplan/planning/script/builders:worker_pool_builder",
        "//nuplan/planning/script/builders/utils:utils_config",
        "//nuplan/planning/training/data_augmentation:kinematic_agent_augmentation",
        "//nuplan/planning/training/data_loader:log_splitter",
        "//nuplan/planning/training/experiments:cache_metadata_entry",
        "//nuplan/planning/training/modeling/models:raster_model",
        "//nuplan/planning/utils/multithreading:worker_pool",
    ],
)

py_test(
    name = "test_model_build",
    size = "medium",
    srcs = ["test_model_build.py"],
    data = [
        "//nuplan/planning/script:yaml",
    ],
    deps = [
        "//nuplan/planning/script/builders:model_builder",
        "//nuplan/planning/script/builders:worker_pool_builder",
        "//nuplan/planning/script/builders/utils:utils_config",
        "//nuplan/planning/training/modeling:torch_module_wrapper",
        "//nuplan/planning/training/modeling/models:lanegcn_model",
        "//nuplan/planning/training/modeling/models:raster_model",
        "//nuplan/planning/training/modeling/models:simple_vector_map_model",
        "//nuplan/planning/training/preprocessing/feature_builders:abstract_feature_builder",
        "//nuplan/planning/training/preprocessing/target_builders:abstract_target_builder",
    ],
)

py_test(
    name = "test_run_simulation",
    size = "small",
    srcs = ["test_run_simulation.py"],
    data = [
        "//nuplan/planning/script:yaml",
    ],
    deps = [
        ":skeleton_test_simulation",
    ],
)

py_test(
    name = "test_run_challenge",
    size = "small",
    srcs = ["test_run_challenge.py"],
    data = [
        "//nuplan/planning/script:yaml",
    ],
    flaky = True,
    deps = [
        ":skeleton_test_simulation",
    ],
)

py_test(
    name = "test_run_ray_worker",
    size = "small",
    srcs = ["test_run_ray_worker.py"],
    data = [
        "//nuplan/planning/script:yaml",
    ],
    deps = [
        ":skeleton_test_simulation",
    ],
)

py_test(
    name = "test_run_parallel_worker",
    size = "small",
    srcs = ["test_run_parallel_worker.py"],
    data = [
        "//nuplan/planning/script:yaml",
    ],
    deps = [
        ":skeleton_test_simulation",
    ],
)

py_test(
    name = "test_run_sequential_worker",
    size = "small",
    srcs = ["test_run_sequential_worker.py"],
    data = [
        "//nuplan/planning/script:yaml",
    ],
    deps = [
        ":skeleton_test_simulation",
    ],
)

py_test(
    name = "test_run_metric",
    size = "small",
    srcs = ["test_run_metric.py"],
    data = [
        "//nuplan/planning/script:yaml",
    ],
    deps = [
        ":skeleton_test_simulation",
        "//nuplan/planning/script:run_metric",
        "//nuplan/planning/script:run_metric_aggregator",
    ],
)

py_test(
    name = "test_run_nuboard",
    size = "medium",
    srcs = ["test_run_nuboard.py"],
    data = [
        "//nuplan/planning/script:yaml",
    ],
    deps = [
        "//nuplan/planning/metrics/evaluation_metrics/common:ego_acceleration",
        "//nuplan/planning/metrics/evaluation_metrics/common:ego_jerk",
        "//nuplan/planning/scenario_builder/nuplan_db:nuplan_scenario_builder",
        "//nuplan/planning/script:run_nuboard",
        "//nuplan/planning/script:run_simulation",
        "//nuplan/planning/script/builders:model_builder",
        "//nuplan/planning/script/builders:worker_pool_builder",
        "//nuplan/planning/simulation/controller:log_playback",
        "//nuplan/planning/simulation/controller:perfect_tracking",
        "//nuplan/planning/simulation/observation:idm_agents",
        "//nuplan/planning/simulation/observation:lidar_pc",
        "//nuplan/planning/simulation/observation:tracks_observation",
        "//nuplan/planning/simulation/planner:simple_planner",
        "//nuplan/planning/simulation/simulation_time_controller:step_simulation_time_controller",
        "//nuplan/planning/training/callbacks:profile_callback",
        "//nuplan/planning/training/modeling:lightning_module_wrapper",
    ],
)

py_test(
    name = "test_train_raster_model",
    size = "enormous",
    srcs = ["test_train_raster_model.py"],
    data = [
        "//nuplan/planning/script:yaml",
    ],
    tags = ["manual"],
    deps = [
        "//nuplan/planning/scenario_builder/nuplan_db:nuplan_scenario_builder",
        "//nuplan/planning/script:run_training",
        "//nuplan/planning/script/builders:data_augmentation_builder",
        "//nuplan/planning/script/builders:training_callback_builder",
        "//nuplan/planning/script/builders:training_metrics_builder",
        "//nuplan/planning/script/builders:worker_pool_builder",
        "//nuplan/planning/script/test:skeleton_test_train",
        "//nuplan/planning/training/callbacks:scenario_scoring_callback",
        "//nuplan/planning/training/callbacks/utils:scenario_scene_converter",
        "//nuplan/planning/training/data_augmentation:kinematic_agent_augmentation",
        "//nuplan/planning/training/data_loader:log_splitter",
        "//nuplan/planning/training/modeling/models:raster_model",
    ],
)

py_test(
    name = "test_train_vector_model",
    size = "enormous",
    srcs = ["test_train_vector_model.py"],
    data = [
        "//nuplan/planning/script:yaml",
    ],
    tags = ["manual"],
    deps = [
        "//nuplan/planning/scenario_builder/nuplan_db:nuplan_scenario_builder",
        "//nuplan/planning/script:run_training",
        "//nuplan/planning/script/builders:data_augmentation_builder",
        "//nuplan/planning/script/builders:training_callback_builder",
        "//nuplan/planning/script/builders:training_metrics_builder",
        "//nuplan/planning/script/builders:worker_pool_builder",
        "//nuplan/planning/script/test:skeleton_test_train",
        "//nuplan/planning/training/callbacks:scenario_scoring_callback",
        "//nuplan/planning/training/callbacks/utils:scenario_scene_converter",
        "//nuplan/planning/training/data_augmentation:agent_dropout_augmentation",
        "//nuplan/planning/training/data_augmentation:kinematic_agent_augmentation",
        "//nuplan/planning/training/data_loader:log_splitter",
        "//nuplan/planning/training/modeling/models:lanegcn_model",
        "//nuplan/planning/training/modeling/models:lanegcn_utils",
        "//nuplan/planning/training/modeling/models:simple_vector_map_model",
    ],
)

py_test(
    name = "test_train_overfitting",
    size = "enormous",
    srcs = ["test_train_overfitting.py"],
    data = [
        "//nuplan/planning/script:yaml",
    ],
    tags = [
        "cpu:20",
    ],
    deps = [
        "//nuplan/planning/scenario_builder/nuplan_db:nuplan_scenario_builder",
        "//nuplan/planning/script:run_training",
        "//nuplan/planning/script/builders:data_augmentation_builder",
        "//nuplan/planning/script/builders:training_callback_builder",
        "//nuplan/planning/script/builders:training_metrics_builder",
        "//nuplan/planning/script/builders:worker_pool_builder",
        "//nuplan/planning/script/test:skeleton_test_train",
        "//nuplan/planning/training/callbacks:scenario_scoring_callback",
        "//nuplan/planning/training/callbacks/utils:scenario_scene_converter",
        "//nuplan/planning/training/data_augmentation:kinematic_agent_augmentation",
        "//nuplan/planning/training/data_loader:log_splitter",
        "//nuplan/planning/training/experiments:cache_metadata_entry",
        "//nuplan/planning/training/modeling/models:raster_model",
        "//nuplan/planning/utils/multithreading:worker_pool",
    ],
)

py_test(
    name = "test_cache",
    size = "enormous",
    srcs = ["test_cache.py"],
    data = [
        "//nuplan/planning/script:yaml",
    ],
    tags = ["manual"],
    deps = [
        "//nuplan/planning/scenario_builder/nuplan_db:nuplan_scenario_builder",
        "//nuplan/planning/script:run_training",
        "//nuplan/planning/script/builders:data_augmentation_builder",
        "//nuplan/planning/script/builders:training_callback_builder",
        "//nuplan/planning/script/builders:training_metrics_builder",
        "//nuplan/planning/script/builders:worker_pool_builder",
        "//nuplan/planning/script/test:skeleton_test_train",
        "//nuplan/planning/training/callbacks/utils:scenario_scene_converter",
        "//nuplan/planning/training/data_loader:log_splitter",
        "//nuplan/planning/training/modeling/models:raster_model",
    ],
)

py_test(
    name = "test_one_cycle_lr_scheduler",
    size = "enormous",
    srcs = ["test_one_cycle_lr_scheduler.py"],
    data = [
        "//nuplan/planning/script:yaml",
    ],
    deps = [
        "//nuplan/planning/scenario_builder/nuplan_db:nuplan_scenario_builder",
        "//nuplan/planning/script:run_training",
        "//nuplan/planning/script/builders:data_augmentation_builder",
        "//nuplan/planning/script/builders:training_callback_builder",
        "//nuplan/planning/script/builders:training_metrics_builder",
        "//nuplan/planning/script/builders:worker_pool_builder",
        "//nuplan/planning/script/builders/utils:utils_config",
        "//nuplan/planning/script/test:skeleton_test_train",
        "//nuplan/planning/training/callbacks:scenario_scoring_callback",
        "//nuplan/planning/training/callbacks/utils:scenario_scene_converter",
        "//nuplan/planning/training/data_augmentation:kinematic_agent_augmentation",
        "//nuplan/planning/training/data_loader:log_splitter",
        "//nuplan/planning/training/experiments:cache_metadata_entry",
        "//nuplan/planning/training/modeling/models:lanegcn_utils",
        "//nuplan/planning/training/modeling/models:simple_vector_map_model",
        "//nuplan/planning/utils/multithreading:worker_pool",
    ],
)
