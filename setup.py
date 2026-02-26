import sys
import os
from cx_Freeze import setup, Executable

include_files = [
    ("fonts", "fonts"), 
]

build_exe_options = {
    "packages": ["customtkinter", "pyglet"],
    "include_files": include_files,
    "excludes": [],
}

setup(
    name="Розрахунок судового збору",
    version="1.1",
    description="Розрахунок судового збору — в/ч А3913",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "rozrah.py",
            base="Win32GUI", 
            target_name="rozrah.exe",
        )
    ],
)
