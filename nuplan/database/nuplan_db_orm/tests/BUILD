load("@rules_python//python:defs.bzl", "py_library", "py_test")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "__init__",
    srcs = ["__init__.py"],
)

py_test(
    name = "test_camera",
    size = "small",
    srcs = ["test_camera.py"],
    deps = [
        "//nuplan/database/tests:nuplan_db_test_utils",
    ],
)

py_test(
    name = "test_category",
    size = "small",
    srcs = ["test_category.py"],
    deps = [
        "//nuplan/database/nuplan_db_orm:category",
    ],
)

py_test(
    name = "test_ego_pose",
    size = "small",
    srcs = ["test_ego_pose.py"],
    deps = [
        "//nuplan/database/tests:nuplan_db_test_utils",
    ],
)

py_test(
    name = "test_image",
    size = "small",
    srcs = ["test_image.py"],
    deps = [
        "//nuplan/database/tests:nuplan_db_test_utils",
    ],
)

py_test(
    name = "test_lidar",
    size = "small",
    srcs = ["test_lidar.py"],
    deps = [
        "//nuplan/database/tests:nuplan_db_test_utils",
    ],
)

py_test(
    name = "test_lidar_box",
    size = "small",
    srcs = ["test_lidar_box.py"],
    deps = [
        "//nuplan/database/nuplan_db_orm:lidar_box",
        "//nuplan/database/nuplan_db_orm:rendering_utils",
        "//nuplan/database/tests:nuplan_db_test_utils",
        "//nuplan/database/utils:geometry",
    ],
)

py_test(
    name = "test_lidar_pc",
    size = "small",
    srcs = ["test_lidar_pc.py"],
    deps = [
        "//nuplan/database/nuplan_db_orm:log",
        "//nuplan/database/tests:nuplan_db_test_utils",
    ],
)

py_test(
    name = "test_log",
    size = "small",
    srcs = ["test_log.py"],
    deps = [
        "//nuplan/database/nuplan_db_orm:log",
    ],
)

py_test(
    name = "test_render",
    size = "small",
    srcs = ["test_render.py"],
    deps = [
        "//nuplan/database/nuplan_db_orm:rendering_utils",
        "//nuplan/database/tests:nuplan_db_test_utils",
    ],
)

py_test(
    name = "test_scenario_tag",
    size = "small",
    srcs = ["test_scenario_tag.py"],
    deps = [
        "//nuplan/database/nuplan_db_orm:scenario_tag",
    ],
)

py_test(
    name = "test_track",
    size = "small",
    srcs = ["test_track.py"],
    deps = [
        "//nuplan/database/tests:nuplan_db_test_utils",
    ],
)

py_test(
    name = "test_traffic_light_status",
    size = "small",
    srcs = ["test_traffic_light_status.py"],
    deps = [
        "//nuplan/database/nuplan_db_orm:traffic_light_status",
    ],
)

py_test(
    name = "test_utils",
    size = "medium",
    srcs = ["test_utils.py"],
    deps = [
        "//nuplan/database/nuplan_db_orm:frame",
        "//nuplan/database/nuplan_db_orm:lidar_box",
        "//nuplan/database/nuplan_db_orm:lidar_pc",
        "//nuplan/database/nuplan_db_orm:nuplandb",
        "//nuplan/database/nuplan_db_orm:utils",
        "//nuplan/database/tests:nuplan_db_test_utils",
        "//nuplan/database/utils/boxes:box3d",
        "//nuplan/database/utils/pointclouds:lidar",
    ],
)

py_test(
    name = "test_nuplandb",
    size = "medium",
    srcs = ["test_nuplandb.py"],
    deps = [
        "//nuplan/database/common:db",
        "//nuplan/database/nuplan_db_orm:nuplandb",
        "//nuplan/database/tests:nuplan_db_test_utils",
    ],
)

py_test(
    name = "test_nuplandb_wrapper",
    size = "medium",
    srcs = ["test_nuplandb_wrapper.py"],
    deps = [
        "//nuplan/database/nuplan_db_orm:nuplandb_wrapper",
        "//nuplan/database/tests:nuplan_db_test_utils",
    ],
)

py_test(
    name = "test_prediction_construction",
    size = "small",
    srcs = ["test_prediction_construction.py"],
    deps = [
        "//nuplan/common/actor_state:waypoint",
        "//nuplan/database/nuplan_db_orm:prediction_construction",
        "//nuplan/planning/simulation/trajectory:trajectory_sampling",
    ],
)

py_test(
    name = "test_scene",
    size = "small",
    srcs = ["test_scene.py"],
    deps = [
        "//nuplan/database/nuplan_db_orm:scene",
    ],
)

py_test(
    name = "test_vector_map_np",
    size = "small",
    srcs = ["test_vector_map_np.py"],
    deps = [
        "//nuplan/database/nuplan_db_orm:vector_map_np",
    ],
)
