load("@rules_python//python:defs.bzl", "py_test")

package(default_visibility = ["//visibility:public"])

py_test(
    name = "test_tutorial_utils",
    size = "small",
    srcs = ["test_tutorial_utils.py"],
    tags = ["manual"],
    deps = [
        "//nuplan/database/tests:nuplan_db_test_utils",
        "//tutorials/utils:tutorial_utils",
    ],
)
