import time
import psutil
import json
from notifier import show_popup
import os
import sys


def app_path(filename):
    """Return the path to a file stored next to the executable."""
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, filename)


SETTINGS_FILE = app_path("settings.json")


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"threshold": 90}, f, indent=4)

    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


# Holds the state of whether the user has already been notified about the battery level
already_notified = False

# Checks the battery status in a loop
while True:
    # Define the battery threshold percentage
    settings = load_settings()
    THRESHOLD = settings["threshold"]

    # Get the battery status
    battery = psutil.sensors_battery()
    if battery:
        if (battery.power_plugged and battery.percent >= THRESHOLD and not already_notified):
            choice = show_popup(
                "To help preserve battery health,\n"
                "consider unplugging the charger.",
                battery.percent, THRESHOLD)
            already_notified = True

        if battery.percent < THRESHOLD:
            already_notified = False

# Checks the battery status every 3 minutes (180 seconds)
    time.sleep(180)