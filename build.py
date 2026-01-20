"""
Build script for creating standalone EXE using PyInstaller
"""
import PyInstaller.__main__
import shutil
import os
from pathlib import Path


def build_exe():
    """Build the application as a standalone EXE"""

    # Get project directory
    project_dir = Path(__file__).parent

    # Define paths
    main_script = str(project_dir / "main.py")
    demo_folder = str(project_dir / "demo")
    assets_folder = str(project_dir / "assets")

    # PyInstaller arguments
    args = [
        main_script,
        '--name=VariantFileGenerator',
        '--onefile',
        '--windowed',
        '--icon=NONE',
        f'--add-data={demo_folder};demo',
        f'--add-data={assets_folder};assets',
        '--hidden-import=customtkinter',
        '--hidden-import=PIL._tkinter_finder',
        '--collect-all=customtkinter',
        '--noconfirm',
        '--clean',
    ]

    print("Building EXE with PyInstaller...")
    PyInstaller.__main__.run(args)

    # Copy demo_writeheader.bat to dist folder
    dist_dir = project_dir / "dist"
    bat_file = project_dir / "demo" / "demo_writeheader.bat"

    if bat_file.exists() and dist_dir.exists():
        shutil.copy(bat_file, dist_dir / "demo_writeheader.bat")
        print(f"\nCopied demo_writeheader.bat to {dist_dir}")

    print(f"\nBuild completed!")
    print(f"EXE location: {dist_dir / 'VariantFileGenerator.exe'}")
    print(f"Remember: demo_writeheader.bat must be in the same directory as the EXE")


if __name__ == "__main__":
    build_exe()
