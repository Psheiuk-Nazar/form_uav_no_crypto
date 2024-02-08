import json
from typing import Any
import os
import threading
import platform
from flask_wtf import CSRFProtect
from flask import Flask, render_template, jsonify, request
import glob
import subprocess
import psutil
from utils.base_info import dt_auto_fl, made_mission_file, config
from utils.read_tasks import change_mission_parameter
from utils.forms import CoordinatesForm

app = Flask(__name__, template_folder="templates")

app.config["SECRET_KEY"] = config["form"]["secret_key"]

csrf = CSRFProtect(app)


def mission_status():
    if os.path.exists(config["form"]["mission_save_path"] + os.sep + "mission.json"):
        return "Mission file exists"
    else:
        return "Mission file doesn't exist"


def mission_execution_status():
    status = "Not running"
    for proc in psutil.process_iter():
        try:
            if config["form"]["mission_executor"] in proc.cmdline():
                status = "Running"
                break
        except:
            pass
    return status


@app.route("/")
def index() -> Any:
    return render_template("pages/index.html",
                           mission_status=mission_status(),
                           mission_execution_status=mission_execution_status(),
                           )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html'), 404


@app.route("/gps_mission/", methods=["GET", "POST"])
def gps_mission():
    form = CoordinatesForm()
    return render_template("forms/form_1.2.html", form=form)


@app.route("/mission_gps/save_gps/", methods=["POST"])
def save_coordinates_to_file() -> Any:
    start_coordinate = request.form["start_coordinate"]
    end_coordinate = request.form["end_coordinate"]
    finish_yaw = float(request.form["finish_yaw"])
    fly_altitude = int(request.form["fly_altitude"])
    gpio = config["form"]["gpio_buzzer"]

    coordinates_to_file = {
        "start": [float(_.strip()) for _ in list(start_coordinate.split(","))],
        "end": [float(_.strip()) for _ in list(end_coordinate.split(","))],
        "finish_yaw": finish_yaw,
        "fly_altitude": fly_altitude,
        "gpio": gpio
    }
    try:
        change_mission_parameter(coordinates_to_file)
        return render_template("forms/coordinates_saved.html", info=coordinates_to_file)
    except:
        return render_template("pages/error_encrypted.html", param="Save coordinates")


@app.route("/map/", methods=["GET", "POST"])
def show_map() -> Any:
    info = dt_auto_fl()
    latitude, longitude = info["start"][0], info["start"][1]

    end = [info["end"][0], info["end"][1]]

    return render_template("map.html", latitude=latitude, longitude=longitude, end=end)


@app.route("/get_data/")
def get_data() -> json:
    try:
        return jsonify(dt_auto_fl())
    except FileNotFoundError:
        made_mission_file()
        return get_data


def proces():
    # subprocess.run(["/bin/bash", " -c \"" + config["form"].get("mission_executor") + "\""])
    query = config["form"].get("mission_executor")
    process = subprocess.Popen(query, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = process.stdout.read() + process.stderr.read()
    print(out.decode("utf-8"))


@app.route("/start_mission", methods=["POST"])
def run_function():
    mission_thread = threading.Thread(target=proces)
    mission_thread.start()

    return render_template("pages/mission_status.html")


@app.route("/get_last_log/", methods=["GET"])
def get_last_log():
    log_directory = config["form"].get("logs_path")
    log_files = [f for f in os.listdir(log_directory) if os.path.isfile(os.path.join(log_directory, f))]
    log_files.sort(key=lambda x: os.path.getmtime(os.path.join(log_directory, x)), reverse=True)

    if log_files:
        last_log_file = os.path.join(log_directory, log_files[0])
        with open(last_log_file, "r") as file:
            log_content = file.read()
    else:
        log_content = "No log files found."

    return jsonify({"log_content": log_content})


if __name__ == "__main__":
    app.run(host=config["form"]["host"], port=config["form"]["port"])
