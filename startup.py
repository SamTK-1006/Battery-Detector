import os
import sys
import win32com.client


def startup_folder():
    return os.path.join(
        os.getenv("APPDATA"),
        r"Microsoft\Windows\Start Menu\Programs\Startup"
    )


def shortcut_path():
    return os.path.join(
        startup_folder(),
        "Battery Detector.lnk"
    )


def enable_startup():

    shell = win32com.client.Dispatch("WScript.Shell")

    shortcut = shell.CreateShortCut(shortcut_path())

    shortcut.Targetpath = sys.executable
    shortcut.WorkingDirectory = os.path.dirname(sys.executable)
    shortcut.IconLocation = sys.executable

    shortcut.save()


def disable_startup():

    path = shortcut_path()

    if os.path.exists(path):
        os.remove(path)


def startup_enabled():

    return os.path.exists(shortcut_path())

if __name__ == "__main__":
    enable_startup()
    print(startup_enabled())