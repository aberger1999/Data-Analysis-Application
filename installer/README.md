# Quick Start: Creating Windows Installer

## ⭐ RECOMMENDED METHOD (Works Best with PyQt6)

### Using PyInstaller + Inno Setup

1. **Build the application:**
   ```powershell
   .\build_installer.ps1
   ```

2. **If you don't have Inno Setup:**
   - Download from: https://jrsoftware.org/isdl.php
   - Install it
   - Run the script again

3. **Done!** Your installer will be at `installer/DataAnalysisApp-Setup-1.0.0.exe`

---

## Alternative: MSI Installer (More Complex)

### Method 1: cx_Freeze (Simple but has PyQt6 issues)

⚠️ **Note:** cx_Freeze has compatibility issues with PyQt6. Use the Inno Setup method above instead.

```bash
pip install cx_Freeze
.\build_msi_simple.ps1
```

### Method 2: WiX Toolset (Professional MSI)

1. Download WiX Toolset from https://wixtoolset.org/
2. Run:
   ```bash
   .\build_msi.bat
   ```

---

## What You Get

✅ Professional Windows installer (.exe or .msi file)
✅ Start Menu shortcuts
✅ Desktop shortcuts
✅ Add/Remove Programs integration
✅ Clean uninstallation
✅ Silent install support

---

## Which Method Should I Use?

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **PyInstaller + Inno Setup** | **Most users** | Easy, works great with PyQt6, small installer | Requires Inno Setup |
| **WiX Toolset** | Enterprise/Corporate | True MSI, Group Policy support | Complex setup |
| **cx_Freeze** | Quick testing | Python-native | PyQt6 compatibility issues |

---

## Updating Your App

1. Make your code changes
2. Update version in `installer/inno_setup.iss` (line 5)
3. Run `.\build_installer.ps1`
4. Distribute the new installer

---

## Full Documentation

See `MSI_INSTALLER_GUIDE.md` for complete instructions and troubleshooting.

---

## Distribution

Share the installer file with users. They can:
- Double-click to install
- Installer handles everything automatically
