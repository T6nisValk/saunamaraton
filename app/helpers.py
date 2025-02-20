# other imports
import os
import sys


def resourcePath(relative_path):
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores the app in there
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    # Build the full path
    full_path = os.path.join(base_path, relative_path)

    # Replace backslashes with forward slashes for Qt compatibility
    return full_path.replace("\\", "/")
