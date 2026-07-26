import time
import psutil
import json
from notifier import show_popup, settings_path
import os
import sys

def load_settings():
    try:
        with open(settings_path(), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        settings = {"threshold": 90}

        with open(settings_path(), "w") as f:
            json.dump(settings, f, indent=4)

        return settings
    

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