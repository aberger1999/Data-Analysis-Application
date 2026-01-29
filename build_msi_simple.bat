@echo off
REM Simple build script for creating MSI using cx_Freeze
REM This is an alternative to WiX that doesn't require external tools

echo ========================================
echo Data Analysis Application MSI Builder
echo Using cx_Freeze
echo ========================================
echo.

REM Install cx_Freeze if not already installed
echo [1/3] Checking cx_Freeze installation...
pip show cx_Freeze >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo cx_Freeze not found. Installing...
    pip install cx_Freeze
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to install cx_Freeze!
        exit /b 1
    )
)
echo cx_Freeze is ready!
echo.

REM Build the MSI
echo [2/3] Building MSI installer...
python setup_msi.py bdist_msi
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: MSI build failed!
    exit /b 1
)
echo MSI installer created successfully!
echo.

REM Find and display the MSI location
echo [3/3] Locating MSI file...
for /r "dist" %%i in (*.msi) do (
    echo.
    echo ========================================
    echo BUILD COMPLETE!
    echo ========================================
    echo MSI installer location: %%i
    echo.
    echo You can now distribute this MSI file to users.
    echo Double-click to install the application.
    echo.
    goto :end
)

echo WARNING: MSI file not found in dist folder!

:end
pause
