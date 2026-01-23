from cx_Freeze import setup, Executable

setup(
    name="Розрахунок судового збору",
    version="1.0",
    description="Your app description",
    executables=[Executable("rozrah.py", base="Win32GUI")]  # Use "Win32GUI" for no console, or None for console
)
