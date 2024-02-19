config_setting(
    name = "_ltl_rules",
    define_values = {
        "ltl_rules": "true",
    },
)

py_library(
    name = "evaluator_stl",
    srcs = ["__init__.py",
            "evaluator_stl.py",
            "base_label_function.py",
            "safe_distance_label_function.py"],
    data = ["@bark_project//bark/python_wrapper:core.so"],
    imports = ["../../external/bark_project/bark/python_wrapper/"],
    visibility = ["//visibility:public"],
)