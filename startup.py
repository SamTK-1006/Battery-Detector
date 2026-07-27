import os
import sys
import win32com.client


# ---------------- Startup Folder ---------------- #

def startup_folder():
    """Return the Windows Startup folder."""
    return os.path.join(
        os.getenv("APPDATA"),
        r"Microsoft\Windows\Start Menu\Programs\Startup"
    )


# ---------------- Shortcut Path ---------------- #

def shortcut_path():
    """Return the Battery Detector shortcut path."""
    return os.path.join(
        startup_folder(),
        "Battery Detector.lnk"
    )


# ---------------- Enable Startup ---------------- #

def enable_startup():
    """Create a startup shortcut for the application."""

    if not getattr(sys, "frozen", False):
        return

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path())

    shortcut.Targetpath = sys.executable
    shortcut.WorkingDirectory = os.path.dirname(sys.executable)
    shortcut.IconLocation = sys.executable

    shortcut.save()


# ---------------- Disable Startup ---------------- #

def disable_startup():
    """Remove the startup shortcut if it exists."""

    path = shortcut_path()

    if os.path.exists(path):
        os.remove(path)


# ---------------- Startup Status ---------------- #

def startup_enabled():
    """Return True if startup is enabled."""
    return os.path.exists(shortcut_path())


if __name__ == "__main__":
    enable_startup()
    print(startup_enabled())