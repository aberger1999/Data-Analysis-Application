# Development Guide

## Quick Start for Development

### Windows Development Setup

1. **Install Python 3.8+** from python.org

2. **Clone and setup**:
```bash
git clone <repository-url>
cd Data-Analysis-Application
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python src/main.py
```

### macOS Development Setup

1. **Install Python 3.8+** (use Homebrew recommended):
```bash
brew install python@3.11
```

2. **Clone and setup**:
```bash
git clone <repository-url>
cd Data-Analysis-Application
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

3. **Run the application**:
```bash
python3 src/main.py
```

## Building Executables

### Windows Build

```bash
# Activate virtual environment
venv\Scripts\activate

# Run build script
build_windows.bat
```

Output: `dist/DataAnalysisApp/DataAnalysisApp.exe`

### macOS Build

```bash
# Activate virtual environment
source venv/bin/activate

# Make script executable and run
chmod +x build_mac.sh
./build_mac.sh
```

Output: `dist/DataAnalysisApp.app`

To create DMG:
```bash
hdiutil create -volname DataAnalysisApp -srcfolder dist/DataAnalysisApp.app -ov -format UDZO dist/DataAnalysisApp.dmg
```

## Creating macOS Icon (.icns)

On macOS, after running `create_icon.py`:

```bash
mkdir icon.iconset
sips -z 16 16     assets/icon_1024x1024.png --out icon.iconset/icon_16x16.png
sips -z 32 32     assets/icon_1024x1024.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     assets/icon_1024x1024.png --out icon.iconset/icon_32x32.png
sips -z 64 64     assets/icon_1024x1024.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   assets/icon_1024x1024.png --out icon.iconset/icon_128x128.png
sips -z 256 256   assets/icon_1024x1024.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   assets/icon_1024x1024.png --out icon.iconset/icon_256x256.png
sips -z 512 512   assets/icon_1024x1024.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   assets/icon_1024x1024.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 assets/icon_1024x1024.png --out icon.iconset/icon_512x512@2x.png
iconutil -c icns icon.iconset -o assets/icon.icns
```

## Testing

Run the application in development mode:
```bash
python src/main.py
```

Test features:
- Load CSV/Excel files
- Create visualizations
- Run statistical analyses
- Export results

## Common Issues

### Windows
- **Missing DLLs**: Install Visual C++ Redistributable
- **Import errors**: Ensure virtual environment is activated

### macOS
- **Permission denied**: Use `chmod +x` on scripts
- **Gatekeeper issues**: Run `xattr -cr` on the app bundle

## Project Structure

```
Data-Analysis-Application/
├── src/
│   ├── main.py              # Entry point
│   └── ui/                  # UI components
│       ├── main_window.py
│       └── components/
├── assets/                  # Icons and resources
├── requirements.txt         # Dependencies
├── data_analysis_app.spec   # PyInstaller config
├── build_windows.bat        # Windows build
├── build_mac.sh            # macOS build
├── setup.py                # Package setup
└── README.md               # User documentation
```
