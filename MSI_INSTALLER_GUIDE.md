# MSI Installer Creation Guide

This guide explains how to create a Windows MSI installer for the Data Analysis Application.

## Overview

Two methods are available for creating MSI installers:

1. **WiX Toolset** (Recommended for professional distribution)
2. **cx_Freeze** (Simpler, Python-native approach)

---

## Method 1: WiX Toolset (Professional)

### Prerequisites

1. **Install WiX Toolset 3.11 or later**
   - Download from: https://wixtoolset.org/
   - Install the WiX Toolset build tools
   - Ensure WiX tools are added to your system PATH

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Building the MSI

Simply run the build script:

```bash
build_msi.bat
```

This script will:
1. Build the application using PyInstaller
2. Generate a file list of all application files
3. Compile the WiX configuration
4. Create the MSI installer
5. Clean up temporary files

**Output:** `installer/DataAnalysisApp-Setup.msi`

### Customization

Edit `installer/wix_config.wxs` to customize:
- Product name and version
- Manufacturer name
- Upgrade GUID (keep consistent across versions)
- Installation directory
- Shortcuts (Start Menu, Desktop)
- License agreement
- Custom branding (icons, banners)

### Important Notes

- **Upgrade Code**: The GUID in `wix_config.wxs` should remain constant across all versions to enable proper upgrades
- **Product ID**: Set to "*" to auto-generate for each build
- **Version Number**: Update in `wix_config.wxs` for each release

---

## Method 2: cx_Freeze (Simple)

### Prerequisites

1. **Install cx_Freeze**
   ```bash
   pip install cx_Freeze
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Building the MSI

Run the simple build script:

```bash
build_msi_simple.bat
```

Or manually:

```bash
python setup_msi.py bdist_msi
```

**Output:** `dist/Data Analysis Application-1.0.0-win64.msi`

### Customization

Edit `setup_msi.py` to customize:
- Application name and version
- Author/company information
- Included packages and files
- Installation options
- Shortcuts and icons

---

## Comparison: WiX vs cx_Freeze

| Feature | WiX Toolset | cx_Freeze |
|---------|-------------|-----------|
| **Setup Complexity** | Moderate | Simple |
| **External Dependencies** | Yes (WiX Toolset) | No (Python only) |
| **Customization** | Extensive | Limited |
| **Professional Features** | Full control | Basic |
| **Upgrade Support** | Excellent | Good |
| **File Size** | Smaller | Larger |
| **Best For** | Professional distribution | Quick testing |

---

## Installation Features

Both methods create MSI installers with:

✅ **Start Menu shortcuts**
✅ **Desktop shortcuts**
✅ **Add/Remove Programs integration**
✅ **Proper uninstallation**
✅ **Windows Installer database**
✅ **Silent installation support** (`msiexec /i installer.msi /quiet`)

---

## Distribution

### Testing the Installer

1. Build the MSI using either method
2. Copy the MSI to a clean Windows machine
3. Double-click to install
4. Verify the application launches correctly
5. Test uninstallation from Control Panel

### Silent Installation

For enterprise deployment:

```bash
msiexec /i DataAnalysisApp-Setup.msi /quiet /norestart
```

### Silent Uninstallation

```bash
msiexec /x DataAnalysisApp-Setup.msi /quiet /norestart
```

---

## Troubleshooting

### WiX Build Errors

**Error: "heat.exe not found"**
- Solution: Install WiX Toolset and add to PATH
- Verify: Run `heat.exe` in command prompt

**Error: "candle.exe failed"**
- Check `wix_config.wxs` for XML syntax errors
- Ensure all file paths are correct

**Error: "light.exe failed"**
- Check for duplicate component IDs
- Verify all referenced files exist

### cx_Freeze Build Errors

**Error: "Module not found"**
- Add missing module to `packages` list in `setup_msi.py`

**Error: "DLL load failed"**
- Add missing DLLs to `include_files` in `setup_msi.py`

### Installation Errors

**Error: "Another version is already installed"**
- Uninstall the existing version first
- Or increment the version number

**Error: "Installation failed"**
- Run as Administrator
- Check Windows Event Viewer for details
- Verify disk space availability

---

## Version Updates

When releasing a new version:

1. **Update version number** in:
   - `wix_config.wxs` (WiX method)
   - `setup_msi.py` (cx_Freeze method)

2. **Keep the Upgrade Code the same** (for proper upgrades)

3. **Rebuild the MSI**

4. **Test the upgrade** on a machine with the old version installed

---

## Advanced Customization

### Adding Custom Icons

1. Create/obtain an `.ico` file
2. Place in `assets/icon.ico`
3. Reference in configuration files

### Custom Installation Directory

**WiX:** Edit `INSTALLFOLDER` in `wix_config.wxs`

**cx_Freeze:** Edit `initial_target_dir` in `setup_msi.py`

### Adding File Associations

Edit `wix_config.wxs` to add file type associations (e.g., `.csv`, `.xlsx`)

### Custom Dialogs

WiX supports custom installation dialogs - see WiX documentation for details

---

## Best Practices

1. ✅ **Test on clean Windows installations**
2. ✅ **Use consistent version numbering** (semantic versioning)
3. ✅ **Keep upgrade codes constant** across versions
4. ✅ **Sign your MSI** with a code signing certificate (for production)
5. ✅ **Include license agreement** and documentation
6. ✅ **Test both installation and uninstallation**
7. ✅ **Verify shortcuts work correctly**
8. ✅ **Check for missing dependencies**

---

## Code Signing (Optional but Recommended)

For production distribution, sign your MSI:

```bash
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com DataAnalysisApp-Setup.msi
```

Benefits:
- Removes "Unknown Publisher" warnings
- Builds user trust
- Required for some enterprise environments

---

## Support

For issues or questions:
- Check the troubleshooting section above
- Review WiX documentation: https://wixtoolset.org/documentation/
- Review cx_Freeze documentation: https://cx-freeze.readthedocs.io/

---

## Quick Start

**Fastest way to create an MSI:**

```bash
# Install cx_Freeze
pip install cx_Freeze

# Build MSI
build_msi_simple.bat
```

**For professional distribution:**

```bash
# Install WiX Toolset from https://wixtoolset.org/

# Build MSI
build_msi.bat
```

Done! Your MSI installer is ready for distribution.
