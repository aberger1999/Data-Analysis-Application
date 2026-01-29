from cx_Freeze import setup, Executable
import sys

build_exe_options = {
    "packages": [
        "PyQt6",
        "PyQt6.QtCore",
        "PyQt6.QtGui",
        "PyQt6.QtWidgets",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "scipy",
        "openpyxl",
        "xlrd",
    ],
    "includes": [
        "PyQt6.QtCore",
        "PyQt6.QtGui",
        "PyQt6.QtWidgets",
        "PyQt6.sip",
    ],
    "excludes": [
        "tkinter",
        "unittest",
        "email",
        "http",
        "xml",
        "pydoc",
        "test",
    ],
    "include_files": [],
    "optimize": 2,
    "zip_include_packages": ["*"],
    "zip_exclude_packages": ["PyQt6"],
}

bdist_msi_options = {
    "upgrade_code": "{12345678-1234-1234-1234-123456789012}",
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\Data Analysis Application",
    "summary_data": {
        "author": "Your Company Name",
        "comments": "Professional data analysis and visualization tool",
        "keywords": "data analysis, visualization, statistics",
    },
}

base = None
if sys.platform == "win32":
    base = "gui"

executables = [
    Executable(
        "src/main.py",
        base=base,
        target_name="DataAnalysisApp.exe",
        shortcut_name="Data Analysis Application",
        shortcut_dir="ProgramMenuFolder",
    )
]

setup(
    name="Data Analysis Application",
    version="1.0.0",
    description="Professional data analysis and visualization tool",
    author="Your Company Name",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=executables,
)
