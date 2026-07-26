import time
import psutil
import json
from notifier import show_popup, settings_path
import os
import sys
import pystray
from PIL import Image
import threading

def resource_path(relative_path):
    """Return the correct path for bundled resources."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

running = True

def quit_app(icon, item):
    global running
    running = False
    icon.stop()
    os._exit(0)


def create_tray():
    image = Image.open(resource_path("assets/logo.ico"))

    menu = pystray.Menu(
        pystray.MenuItem("Exit", quit_app)
    )

    icon = pystray.Icon(
        "BatteryDetector",
        image,
        "Battery Detector",
        menu
    )

    icon.run()


def start_tray():
    threading.Thread(target=create_tray, daemon=True).start()

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

def battery_monitor():
    global already_notified

    while running:

        settings = load_settings()
        THRESHOLD = settings["threshold"]

        battery = psutil.sensors_battery()

        if battery:
            if (
                battery.power_plugged
                and battery.percent >= THRESHOLD
                and not already_notified
            ):

                choice = show_popup(
                    "To help preserve battery health,\n"
                    "consider unplugging the charger.",
                    battery.percent,
                    THRESHOLD,
                )

                already_notified = True

            if battery.percent < THRESHOLD:
                already_notified = False

        time.sleep(180)

start_tray()

battery_thread = threading.Thread(
    target=battery_monitor,
    daemon=True
)

battery_thread.start()
battery_thread.join()