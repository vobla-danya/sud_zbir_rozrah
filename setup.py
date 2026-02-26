import sys
import os
from cx_Freeze import setup, Executable, BuildExeOptions

include_files = [
    ("fonts", "fonts"),
]

build_exe_options = BuildExeOptions(
    packages=["customtkinter", "pyglet"],
    include_files=include_files,
)

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
