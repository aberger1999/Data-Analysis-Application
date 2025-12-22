@echo off
REM Launcher script for Data Analysis Application
REM This ensures the virtual environment's DLLs are prioritized

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Ensure venv's Scripts directory is first in PATH to prioritize its DLLs
set "PATH=%CD%\venv\Scripts;%PATH%"

REM Run the application
python src\main.py

