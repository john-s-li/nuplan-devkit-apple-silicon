load("@rules_python//python:defs.bzl", "py_library")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "checkpoint_callback",
    srcs = ["checkpoint_callback.py"],
)

py_library(
    name = "profile_callback",
    srcs = ["profile_callback.py"],
    deps = [
    ],
)

py_library(
    name = "time_logging_callback",
    srcs = ["time_logging_callback.py"],
)

py_library(
    name = "validate_setup_callback",
    srcs = ["validate_setup_callback.py"],
    deps = [
        "//nuplan/planning/training/data_loader:datamodule",
        "//nuplan/planning/training/modeling:lightning_module_wrapper",
    ],
)

py_library(
    name = "scenario_scoring_callback",
    srcs = ["scenario_scoring_callback.py"],
    deps = [
        "//nuplan/planning/training/callbacks/utils:scene_converter",
        "//nuplan/planning/training/data_loader:scenario_dataset",
        "//nuplan/planning/training/modeling:types",
        "//nuplan/planning/training/preprocessing:feature_collate",
    ],
)

py_library(
    name = "visualization_callback",
    srcs = ["visualization_callback.py"],
    deps = [
        "//nuplan/planning/training/callbacks/utils:visualization_utils",
        "//nuplan/planning/training/modeling:types",
        "//nuplan/planning/training/preprocessing:feature_collate",
    ],
)
