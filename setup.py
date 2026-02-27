import sys
import os
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["customtkinter", "pyglet"],
    "include_files": [
        ("fonts", "fonts"),
        ("config.toml", "config.toml")
    ],
}

setup(
    name="rozrah",
    executables=[
        Executable(
            "rozrah.py",
            base="Win32GUI",
            target_name="rozrah.exe",
        )
    ],
    options={"build_exe": build_exe_options},
)
