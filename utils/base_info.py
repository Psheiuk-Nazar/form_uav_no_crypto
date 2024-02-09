import argparse
import json
import os

class CantCreateFileError(Exception):
    pass

parser = argparse.ArgumentParser(
        description="UAV form",
    )
parser.add_argument("-c", "--config", help="Config file", required=True)
args = parser.parse_args()
config = json.loads(open(args.config).read())

mission = {
    "TAKE_OFF_COMMAND": "take_off",
    "START_COMMAND": "start",
    "WAY_TO_POINT_COMMAND": "way_to_point",
    "CONDITION_YAW_COMMAND": "condition_yaw",
    "BEEP_COMMAND": "beep",
    "INFO_COMMAND": "final_info",
    "MODE_COMMAND": "set_mode",
    "MODE_FINISH": "finish_mission"
}


gps_form_name = f"{config['form']['mission_save_path']}" + "mission.json"


def read_json_file(name) :
    try:
        with open(name, "r") as conf:
            return json.load(conf)
    except FileNotFoundError:
        made_mission_file()
        return read_json_file(name)

def made_mission_file()->None:
    mission_commands = [
        {"cmd": mission["BEEP_COMMAND"], "params": {"gpio": config["form"]["gpio_buzzer"]}},
        {"cmd": mission["MODE_COMMAND"], "params": {"mode": "ALT_HOLD"}},
        {"cmd": mission["TAKE_OFF_COMMAND"], "params": {"altitude": 100}},
        {"cmd": mission["START_COMMAND"], "params": {"position": [48.0674, 12.86269304]}},
        {"cmd": mission["WAY_TO_POINT_COMMAND"], "params": {"goal_position": [48.05192, 12.8378]}},
        {"cmd": mission["CONDITION_YAW_COMMAND"], "params": {"yaw_goal": 100}},
        {"cmd": mission["INFO_COMMAND"]},
        {"cmd": mission["MODE_COMMAND"], "params": {"mode": "LAND"}},
        {"cmd": mission["MODE_FINISH"]}
    ]
    try:
        json_data = json.dumps(mission_commands, indent=4)
        with open(gps_form_name, 'w') as file:
            file.write(json_data)
    except Exception as e:
        raise CantCreateFileError(f"Error creating mission file: {e}")

def dt_auto_fl() -> dict:
    file = read_json_file(gps_form_name)
    mission_data = {
            "start": [i.get("params").get("position") for i in file if "start" in i.values()][0],
            "end": [i.get("params").get("goal_position") for i in file if "way_to_point" in i.values()][0],
            "finish_yaw": [i.get("params").get("yaw_goal") for i in file if "condition_yaw" in i.values()][0],
            "fly_altitude": [i.get("params").get("altitude") for i in file if "take_off" in i.values()][0],
    }
    return mission_data
