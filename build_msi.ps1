# Build script for creating MSI installer using WiX Toolset
# Prerequisites: WiX Toolset 3.11+ must be installed
# Download from: https://wixtoolset.org/

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Data Analysis Application MSI Builder" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Build the application with PyInstaller
Write-Host "[1/5] Building application with PyInstaller..." -ForegroundColor Yellow
pyinstaller data_analysis_app.spec --clean --noconfirm
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: PyInstaller build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "Application built successfully!" -ForegroundColor Green
Write-Host ""

# Step 2: Generate file list using WiX Heat tool
Write-Host "[2/5] Generating file list with WiX Heat..." -ForegroundColor Yellow
if (-not (Test-Path "installer")) {
    New-Item -ItemType Directory -Path "installer" | Out-Null
}
heat.exe dir "dist\data_analysis_app" -cg DistFiles -gg -sfrag -srd -dr INSTALLFOLDER -var var.DistDir -out "installer\files.wxs"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: WiX Heat failed! Make sure WiX Toolset is installed and in PATH." -ForegroundColor Red
    Write-Host "Download from: https://wixtoolset.org/" -ForegroundColor Yellow
    exit 1
}
Write-Host "File list generated successfully!" -ForegroundColor Green
Write-Host ""

# Step 3: Compile WiX source files
Write-Host "[3/5] Compiling WiX configuration..." -ForegroundColor Yellow
if (-not (Test-Path "installer\build")) {
    New-Item -ItemType Directory -Path "installer\build" | Out-Null
}
candle.exe -dDistDir="dist\data_analysis_app" "installer\wix_config.wxs" "installer\files.wxs" -out "installer\build\\" -arch x64
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: WiX Candle compilation failed!" -ForegroundColor Red
    exit 1
}
Write-Host "WiX files compiled successfully!" -ForegroundColor Green
Write-Host ""

# Step 4: Link and create MSI
Write-Host "[4/5] Creating MSI installer..." -ForegroundColor Yellow
light.exe -ext WixUIExtension "installer\build\wix_config.wixobj" "installer\build\files.wixobj" -out "installer\DataAnalysisApp-Setup.msi"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: WiX Light linking failed!" -ForegroundColor Red
    exit 1
}
Write-Host "MSI installer created successfully!" -ForegroundColor Green
Write-Host ""

# Step 5: Cleanup
Write-Host "[5/5] Cleaning up temporary files..." -ForegroundColor Yellow
Remove-Item "installer\build\*.wixobj" -ErrorAction SilentlyContinue
Remove-Item "installer\build\*.wixpdb" -ErrorAction SilentlyContinue
Write-Host "Cleanup complete!" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "BUILD COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "MSI installer location: installer\DataAnalysisApp-Setup.msi" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now distribute this MSI file to users." -ForegroundColor White
Write-Host "Double-click to install the application." -ForegroundColor White
Write-Host ""

Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
