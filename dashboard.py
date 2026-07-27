import customtkinter as ctk
import psutil
import os
import sys
from startup import (enable_startup, disable_startup, startup_enabled)

# ---------------- Appearance ---------------- #
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BACKGROUND = "#F8F9FC"
PRIMARY = "#D16BA5"
PRIMARY_HOVER = "#BC5A95"
SECONDARY = "#F2D9E6"

TEXT = "#2D3142"
SUBTEXT = "#6B7280"


def resource_path(relative_path):
    """Return the correct path for bundled resources."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def open_dashboard():
    app = ctk.CTk()
    app.title("Battery Detector")
    app.geometry("360x320")
    app.resizable(False, False)
    app.configure(fg_color=BACKGROUND)
    app.iconbitmap(resource_path("assets/logo.ico"))

    # ---------------- Center Window ---------------- #

    width = 360
    height = 330

    screen_w = app.winfo_screenwidth()
    screen_h = app.winfo_screenheight()

    x = (screen_w - width) // 2
    y = (screen_h - height) // 2

    app.geometry(f"{width}x{height}+{x}+{y}")
    app.grid_columnconfigure(0, weight=1)

    # ---------------- Title ---------------- #

    title = ctk.CTkLabel(
        app,
        text="Battery Detector",
        font=("Segoe UI", 26, "bold"),
        text_color=PRIMARY
    )
    title.grid(row=0, column=0, pady=(25, 10))

    # ---------------- Battery Percentage ---------------- #

    battery_label = ctk.CTkLabel(
        app,
        text="--%",
        font=("Segoe UI", 46, "bold"),
        text_color=TEXT
    )
    battery_label.grid(row=1, column=0)

    # ---------------- Progress Bar ---------------- #

    progress = ctk.CTkProgressBar(
        app,
        width=250,
        height=18,
        progress_color=PRIMARY
    )
    progress.grid(row=2, column=0, pady=(15, 18))

    # ---------------- Status ---------------- #

    status_label = ctk.CTkLabel(
        app,
        text="Status: --",
        font=("Segoe UI", 15),
        text_color=SUBTEXT
    )
    status_label.grid(row=3, column=0)

    # ---------------- Update ---------------- #

    def update():

        battery = psutil.sensors_battery()

        if battery is not None:

            battery_label.configure(
                text=f"{battery.percent:.0f}%"
            )

            progress.set(battery.percent / 100)

            if battery.power_plugged:
                status = "Charging ⚡"
            else:
                status = "Not Charging - On Battery🔋"

            status_label.configure(
                text=f"Status: {status}"
            )

        else:
            battery_label.configure(text="N/A")
            status_label.configure(text="Battery not detected")
            progress.set(0)

        app.after(3000, update)

    update()

    def toggle_startup():
        if startup_checkbox.get():
            enable_startup()
        else:
            disable_startup()

    startup_checkbox = ctk.CTkCheckBox(
    app,
    text="Start with Windows",
    command=toggle_startup,
    text_color=TEXT,
    fg_color=PRIMARY,
    hover_color=PRIMARY_HOVER,
    border_color=PRIMARY,
    checkmark_color="white"
    )

    startup_checkbox.grid(row=4, column=0, pady=(20, 10))

    if startup_enabled():
        startup_checkbox.select()
    else:
        startup_checkbox.deselect()

    # ---------------- Close Button ---------------- #

    close_button = ctk.CTkButton(
        app,
        text="Close",
        width=160,
        height=40,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        corner_radius=12,
        command=app.destroy
    )
    close_button.grid(row=5, column=0, pady=(10, 20))

    app.mainloop()
