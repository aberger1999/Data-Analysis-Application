#!/bin/bash
# Build script for creating MSI installer using WiX Toolset
# Prerequisites: WiX Toolset 3.11+ must be installed
# Download from: https://wixtoolset.org/

echo "========================================"
echo "Data Analysis Application MSI Builder"
echo "========================================"
echo ""

# Step 1: Build the application with PyInstaller
echo "[1/5] Building application with PyInstaller..."
pyinstaller data_analysis_app.spec --clean --noconfirm
if [ $? -ne 0 ]; then
    echo "ERROR: PyInstaller build failed!"
    exit 1
fi
echo "Application built successfully!"
echo ""

# Step 2: Generate file list using WiX Heat tool
echo "[2/5] Generating file list with WiX Heat..."
mkdir -p installer
heat.exe dir "dist/data_analysis_app" -cg DistFiles -gg -sfrag -srd -dr INSTALLFOLDER -var var.DistDir -out "installer/files.wxs"
if [ $? -ne 0 ]; then
    echo "ERROR: WiX Heat failed! Make sure WiX Toolset is installed and in PATH."
    echo "Download from: https://wixtoolset.org/"
    exit 1
fi
echo "File list generated successfully!"
echo ""

# Step 3: Compile WiX source files
echo "[3/5] Compiling WiX configuration..."
mkdir -p installer/build
candle.exe -dDistDir="dist/data_analysis_app" "installer/wix_config.wxs" "installer/files.wxs" -out "installer/build/" -arch x64
if [ $? -ne 0 ]; then
    echo "ERROR: WiX Candle compilation failed!"
    exit 1
fi
echo "WiX files compiled successfully!"
echo ""

# Step 4: Link and create MSI
echo "[4/5] Creating MSI installer..."
light.exe -ext WixUIExtension "installer/build/wix_config.wixobj" "installer/build/files.wixobj" -out "installer/DataAnalysisApp-Setup.msi"
if [ $? -ne 0 ]; then
    echo "ERROR: WiX Light linking failed!"
    exit 1
fi
echo "MSI installer created successfully!"
echo ""

# Step 5: Cleanup
echo "[5/5] Cleaning up temporary files..."
rm -f installer/build/*.wixobj
rm -f installer/build/*.wixpdb
echo "Cleanup complete!"
echo ""

echo "========================================"
echo "BUILD COMPLETE!"
echo "========================================"
echo "MSI installer location: installer/DataAnalysisApp-Setup.msi"
echo ""
echo "You can now distribute this MSI file to users."
echo "Double-click to install the application."
echo ""
