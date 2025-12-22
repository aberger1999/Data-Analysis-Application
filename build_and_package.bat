@echo off
REM Combined script to build and package the Data Analysis Application
REM This will build the executable if needed, then create a distributable ZIP

echo ========================================
echo Data Analysis Application - Build and Package
echo ========================================
echo.

REM Check if executable already exists
if exist "dist\DataAnalysisApp\DataAnalysisApp.exe" (
    echo Executable found. Skipping build step.
    echo.
    goto :package
)

echo Executable not found. Building application...
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Check if Python is available
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again.
    echo.
    pause
    exit /b 1
)

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build the application
echo.
echo Building application with PyInstaller...
echo This may take several minutes...
echo.
pyinstaller data_analysis_app.spec

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed!
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo Build successful!
echo.

:package
REM Now package for distribution
echo ========================================
echo Packaging for distribution...
echo ========================================
echo.

REM Verify executable exists
if not exist "dist\DataAnalysisApp\DataAnalysisApp.exe" (
    echo ERROR: DataAnalysisApp.exe not found after build!
    pause
    exit /b 1
)

REM Create release folder
set RELEASE_DIR=release
if exist "%RELEASE_DIR%" rmdir /s /q "%RELEASE_DIR%"
mkdir "%RELEASE_DIR%"

REM Copy the entire DataAnalysisApp folder
echo Copying application files...
xcopy /E /I /Y "dist\DataAnalysisApp" "%RELEASE_DIR%\DataAnalysisApp"

REM Create a README for end users
echo Creating README for end users...
(
echo Data Analysis Application
echo =========================
echo.
echo INSTALLATION:
echo ------------
echo 1. Extract this ZIP file to any location on your computer
echo 2. Navigate to the DataAnalysisApp folder
echo 3. Double-click DataAnalysisApp.exe to run the application
echo.
echo SYSTEM REQUIREMENTS:
echo -------------------
echo - Windows 10 or later
echo - No additional software required - everything is included!
echo.
echo TROUBLESHOOTING:
echo ---------------
echo If the application doesn't start:
echo - Make sure you extracted ALL files from the ZIP
echo - Try running as administrator
echo - Install Visual C++ Redistributable if needed:
echo   https://aka.ms/vs/17/release/vc_redist.x64.exe
echo.
echo For support, please visit the project repository.
) > "%RELEASE_DIR%\README.txt"

REM Create ZIP file
echo Creating ZIP archive...
set ZIP_NAME=DataAnalysisApp-Windows-v1.0.0.zip
if exist "%ZIP_NAME%" del "%ZIP_NAME%"

REM Use PowerShell to create ZIP (available on Windows 10+)
powershell -Command "Compress-Archive -Path '%RELEASE_DIR%\*' -DestinationPath '%ZIP_NAME%' -Force"

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! Package created!
    echo ========================================
    echo.
    echo Distribution package: %ZIP_NAME%
    echo.
    echo This ZIP file contains everything needed to run the application.
    echo Users can simply extract it and run DataAnalysisApp.exe
    echo.
    echo File location: %CD%\%ZIP_NAME%
    echo.
    for %%A in ("%ZIP_NAME%") do (
        set /a size_mb=%%~zA/1048576
        echo File size: %%~zA bytes ^(~!size_mb! MB^)
    )
    echo.
    echo You can now distribute this ZIP file to users!
    echo.
) else (
    echo.
    echo ERROR: Failed to create ZIP file!
    echo You can manually zip the contents of the '%RELEASE_DIR%' folder.
    echo.
)

REM Clean up release folder (optional - comment out if you want to keep it)
echo Cleaning up temporary files...
rmdir /s /q "%RELEASE_DIR%"

echo.
echo Done!
echo.
pause

