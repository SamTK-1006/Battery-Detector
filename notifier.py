import customtkinter as ctk
import winsound
import json
import os
import sys

# ---------------- Resource Path ---------------- #

def resource_path(relative_path):
    """Return the correct path for bundled resources."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ---------------- Settings Path ---------------- #

def settings_path():
    """Return the path to settings.json in AppData."""
    appdata = os.getenv("LOCALAPPDATA")
    folder = os.path.join(appdata, "BatteryDetector")

    os.makedirs(folder, exist_ok=True)

    return os.path.join(folder, "settings.json")


# ---------------- Appearance ---------------- #

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BACKGROUND = "#F8F9FC"
PRIMARY = "#D16BA5"
PRIMARY_HOVER = "#BC5A95"
SECONDARY = "#F2D9E6"

TEXT = "#2D3142"
SUBTEXT = "#6B7280"


# ---------------- Settings ---------------- #

def save_threshold(choice):
    value = int(choice.replace("%", ""))

    with open(settings_path(), "w") as file:
        json.dump(
            {"threshold": value},
            file,
            indent=4
        )

# ---------------- Threshold ---------------- #

def get_threshold():
    try:
        with open(settings_path(), "r") as file:
            settings = json.load(file)
            return settings["threshold"]

    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return 90


# ---------------- Popup ---------------- #

def show_popup(message, percent):

    result = "dismiss"

    app = ctk.CTk()
    app.iconbitmap(resource_path("assets/logo.ico"))

    winsound.PlaySound(
        resource_path("assets/notification.wav"),
        winsound.SND_FILENAME | winsound.SND_ASYNC
    )

    app.title("Battery Detector")
    app.geometry("460x440")
    app.resizable(False, False)
    app.attributes("-topmost", True)
    app.configure(fg_color=BACKGROUND)

    # ---------------- Center Window ---------------- #

    width = 460
    height = 440

    screen_w = app.winfo_screenwidth()
    screen_h = app.winfo_screenheight()

    x = (screen_w - width) // 2
    y = (screen_h - height) // 2

    app.geometry(f"{width}x{height}+{x}+{y}")
    app.grid_columnconfigure(0, weight=1)

    # ---------------- Title ---------------- #

    title = ctk.CTkLabel(
        app,
        text="Battery Alert",
        font=("Segoe UI", 30, "bold"),
        text_color=PRIMARY
    )

    title.grid(row=0, column=0, pady=(25, 8))

    # ---------------- Subtitle ---------------- #

    subtitle = ctk.CTkLabel(
        app,
        text="Your battery has reached the charging limit.",
        font=("Segoe UI", 15),
        text_color=SUBTEXT
    )

    subtitle.grid(row=1, column=0)

    # ---------------- Battery Percentage ---------------- #

    percentage = ctk.CTkLabel(
        app,
        text=f"{percent:.0f}%",
        font=("Segoe UI", 46, "bold"),
        text_color=TEXT
    )

    percentage.grid(row=2, column=0, pady=(11, 10))

    # ---------------- Progress Bar ---------------- #

    progress = ctk.CTkProgressBar(
        app,
        width=340,
        height=18,
        progress_color=PRIMARY
    )

    progress.set(percent / 100)
    progress.grid(row=3, column=0, pady=(10, 18))

    # ---------------- Message ---------------- #

    message_label = ctk.CTkLabel(
        app,
        text=message,
        font=("Segoe UI", 15),
        text_color=TEXT,
        justify="center",
        wraplength=420
    )

    message_label.grid(row=4, column=0, padx=40, pady=(5, 10))

    # ---------------- Buttons ---------------- #

    button_frame = ctk.CTkFrame(
        app,
        fg_color="transparent"
    )

    button_frame.grid(row=5, column=0, pady=(20, 15))

    def dismiss():
        nonlocal result
        result = "dismiss"
        app.destroy()

    def snooze():
        nonlocal result
        result = "snooze"
        app.destroy()

    dismiss_button = ctk.CTkButton(
        button_frame,
        text="Dismiss",
        width=155,
        height=42,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        corner_radius=12,
        command=dismiss
    )

    dismiss_button.grid(row=0, column=0, padx=10)

    snooze_button = ctk.CTkButton(
        button_frame,
        text="Snooze 1 min",
        width=155,
        height=42,
        fg_color=SECONDARY,
        hover_color="#E9C7D8",
        text_color=TEXT,
        corner_radius=12,
        command=snooze
    )

    snooze_button.grid(row=0, column=1, padx=10)

    app.mainloop()
    return result