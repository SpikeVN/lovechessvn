CONFIG_HIVE = {
    # Maximum analyze depth
    "max_depth": 20,
    # Maximum analyze time
    "max_time": 1,
    "response_weight": 1,
}


def get_config(name: str):
    return CONFIG_HIVE[name]
