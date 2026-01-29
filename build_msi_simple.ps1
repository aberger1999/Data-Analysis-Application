# Build script for creating MSI using cx_Freeze
# This is an alternative to WiX that doesn't require external tools

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Data Analysis Application MSI Builder" -ForegroundColor Cyan
Write-Host "Using cx_Freeze" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check and install cx_Freeze if needed
Write-Host "[1/3] Checking cx_Freeze installation..." -ForegroundColor Yellow
$cxFreezeInstalled = pip show cx_Freeze 2>$null
if (-not $cxFreezeInstalled) {
    Write-Host "cx_Freeze not found. Installing..." -ForegroundColor Yellow
    pip install cx_Freeze
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install cx_Freeze!" -ForegroundColor Red
        exit 1
    }
}
Write-Host "cx_Freeze is ready!" -ForegroundColor Green
Write-Host ""

# Step 2: Build the MSI
Write-Host "[2/3] Building MSI installer..." -ForegroundColor Yellow
python setup_msi.py bdist_msi
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: MSI build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "MSI installer created successfully!" -ForegroundColor Green
Write-Host ""

# Step 3: Find and display the MSI location
Write-Host "[3/3] Locating MSI file..." -ForegroundColor Yellow
$msiFile = Get-ChildItem -Path "dist" -Filter "*.msi" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if ($msiFile) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "BUILD COMPLETE!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "MSI installer location: $($msiFile.FullName)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You can now distribute this MSI file to users." -ForegroundColor White
    Write-Host "Double-click to install the application." -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "WARNING: MSI file not found in dist folder!" -ForegroundColor Yellow
}

Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
