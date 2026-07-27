import json
import os
import sys
import threading
import time

import psutil
import pystray
from PIL import Image

from dashboard import open_dashboard
from notifier import show_popup, settings_path

# ---------------- Resource Path ---------------- #

def resource_path(relative_path):
    """Return the correct path for bundled resources."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ---------------- Global Variables ---------------- #

running = True
already_notified = False

# ---------------- Tray Icon ---------------- #

def quit_app(icon, item):
    global running
    running = False
    icon.stop()
    os._exit(0)

def create_tray():
    image = Image.open(resource_path("assets/logo.ico"))

    menu = pystray.Menu(
        pystray.MenuItem(
            "Open Dashboard",
            lambda icon, item: open_dashboard()
        ),
        pystray.Menu.SEPARATOR,
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

# ---------------- Settings ---------------- #

def load_settings():
    settings = {"threshold": 90}

    try:
        with open(settings_path(), "r") as f:
            return json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        with open(settings_path(), "w") as f:
            json.dump(settings, f, indent=4)

        return settings

# ---------------- Battery Monitor ---------------- #

def battery_monitor():
    global already_notified

    while running:

        settings = load_settings()
        threshold = settings["threshold"]

        battery = psutil.sensors_battery()

        if battery:
            if (
                battery.power_plugged
                and battery.percent >= threshold
                and not already_notified
            ):

                show_popup(
                    "To help preserve battery health,\n"
                    "consider unplugging the charger.",
                    battery.percent,
                )

                already_notified = True

            if battery.percent < threshold:
                already_notified = False

        time.sleep(180)


start_tray()

battery_thread = threading.Thread(
    target=battery_monitor,
    daemon=True
)

battery_thread.start()
battery_thread.join()