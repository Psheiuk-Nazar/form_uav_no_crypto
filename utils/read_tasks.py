import json

from utils.base_info import read_json_file, gps_form_name, config


def update_command_parameter(config_data, command_name, param_name, new_value):
    """
     Update the parameter of a specific command in the mission configuration.

     Parameters:
     - config_data: List of dictionaries representing the mission configuration.
     - command_name: Name of the command to update.
     - param_name: Name of the parameter to update.
     - new_value: New value for the parameter.
     """
    command_index = next(
        (index for (index, command) in enumerate(config_data) if command["cmd"] == command_name),
        None
    )
    if command_index is not None:
        config_data[command_index]["params"][param_name] = new_value


def change_mission_parameter(coordinate, config=config):

    """
    Update mission parameters based on the provided coordinate.

    Parameters:
    - coordinate: Dictionary containing coordinate values.
    """

    config_data = read_json_file(gps_form_name)
    update_command_parameter(config_data, config["mission"]["TAKE_OFF_COMMAND"], "altitude", coordinate.get("fly_altitude"))
    update_command_parameter(config_data, config["mission"]["START_COMMAND"], "position", coordinate.get("start"))
    update_command_parameter(config_data, config["mission"]["WAY_TO_POINT_COMMAND"], "goal_position",
                             coordinate.get("end"))
    update_command_parameter(config_data, config["mission"]["CONDITION_YAW_COMMAND"], "yaw_goal",
                             coordinate.get("finish_yaw"))
    update_command_parameter(config_data, config["mission"]["BEEP_COMMAND"], "gpio", coordinate.get("gpio"))

    with open(gps_form_name, "w") as config:
        json.dump(config_data, config, indent=4)
