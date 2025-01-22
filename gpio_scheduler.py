from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import RPi.GPIO as GPIO
import json
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
scheduler = BackgroundScheduler()
scheduler.start()

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Store schedules in a JSON file
SCHEDULE_FILE = "pin_schedules.json"


def load_schedules():
    """Load schedules from JSON file"""
    try:
        if os.path.exists(SCHEDULE_FILE):
            with open(SCHEDULE_FILE, "r") as f:
                data = json.load(f)
                return data.get("schedules", [])
        return []
    except Exception as e:
        print(f"Error loading schedules: {e}")
        return []


def save_schedules(schedules):
    """Save schedules to JSON file"""
    try:
        with open(SCHEDULE_FILE, "w") as f:
            json.dump({"schedules": schedules}, f, indent=2)
    except Exception as e:
        print(f"Error saving schedules: {e}")


def setup_pin(pin):
    """Initialize a GPIO pin as output"""
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # Start with pin off (HIGH)


def control_pin(pin, state):
    """Control a GPIO pin (state: True for ON/LOW, False for OFF/HIGH)"""
    GPIO.output(pin, not state)  # Inverse logic: LOW is ON, HIGH is OFF


@app.route("/schedule", methods=["POST"])
def add_schedule():
    data = request.get_json()

    if not all(k in data for k in ["pin", "label", "on_time", "off_time"]):
        return jsonify({"error": "Missing required fields"}), 400

    pin = int(data["pin"])
    label = data["label"]
    on_time = data["on_time"]
    off_time = data["off_time"]

    # Setup the pin
    setup_pin(pin)

    # Create schedule IDs
    on_job_id = f"pin_{pin}_{on_time}_on"
    off_job_id = f"pin_{pin}_{off_time}_off"

    # Parse HH:MM into hour and minute
    on_hour, on_minute = on_time.split(":")
    off_hour, off_minute = off_time.split(":")

    # Add new schedules
    scheduler.add_job(
        control_pin,
        CronTrigger.from_crontab(f"{on_minute} {on_hour} * * *"),
        id=on_job_id,
        args=[pin, True],
    )

    scheduler.add_job(
        control_pin,
        CronTrigger.from_crontab(f"{off_minute} {off_hour} * * *"),
        id=off_job_id,
        args=[pin, False],
    )

    # Save schedule to file
    schedules = load_schedules()
    new_schedule = {
        "id": data.get("id", f"{pin}_{on_time}_{off_time}"),
        "pin": str(pin),
        "label": label,
        "on_time": on_time,
        "off_time": off_time,
    }
    schedules.append(new_schedule)
    save_schedules(schedules)

    return jsonify({"message": "Schedule added successfully", "schedule": new_schedule})


@app.route("/schedule/<schedule_id>", methods=["DELETE"])
def remove_schedule(schedule_id):
    schedules = load_schedules()
    schedule = next((s for s in schedules if s["id"] == schedule_id), None)

    if schedule:
        pin = int(schedule["pin"])
        on_time = schedule["on_time"]
        off_time = schedule["off_time"]

        # Remove jobs from scheduler
        scheduler.remove_job(f"pin_{pin}_{on_time}_on", ignore_if_not_exists=True)
        scheduler.remove_job(f"pin_{pin}_{off_time}_off", ignore_if_not_exists=True)

        # Remove from saved schedules
        schedules = [s for s in schedules if s["id"] != schedule_id]
        save_schedules(schedules)
        return jsonify({"message": f"Schedule {schedule_id} removed"})

    return jsonify({"error": "Schedule not found"}), 404


@app.route("/schedules", methods=["GET"])
def get_schedules():
    return jsonify({"schedules": load_schedules()})


@app.route("/pin/<int:pin>", methods=["POST"])
def manual_control(pin):
    data = request.get_json()
    if "state" not in data:
        return jsonify({"error": "State not specified"}), 400

    state = bool(data["state"])
    setup_pin(pin)
    control_pin(pin, state)

    return jsonify(
        {
            "message": f'Pin {pin} {"turned ON" if state else "turned OFF"}',
            "pin": pin,
            "state": state,
        }
    )


# Initialize schedules on startup
with app.app_context():
    schedules = load_schedules()
    for schedule in schedules:
        pin = int(schedule["pin"])
        setup_pin(pin)

        # Parse HH:MM into hour and minute
        on_time = schedule["on_time"]
        off_time = schedule["off_time"]
        on_hour, on_minute = on_time.split(":")
        off_hour, off_minute = off_time.split(":")

        # Recreate the schedules
        scheduler.add_job(
            control_pin,
            CronTrigger.from_crontab(f"{on_minute} {on_hour} * * *"),
            id=f"pin_{pin}_{on_time}_on",
            args=[pin, True],
        )

        scheduler.add_job(
            control_pin,
            CronTrigger.from_crontab(f"{off_minute} {off_hour} * * *"),
            id=f"pin_{pin}_{off_time}_off",
            args=[pin, False],
        )


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    finally:
        scheduler.shutdown()
        GPIO.cleanup()
