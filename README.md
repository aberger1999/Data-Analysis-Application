# Data Analysis Application

A modern, cross-platform desktop application for data analysis built with PyQt6. Features a dark theme UI and comprehensive data analysis tools including visualization, statistical analysis, and machine learning capabilities.

## Features

- **Data Import/Export**: Support for CSV, Excel, and other common data formats
- **Data Visualization**: Interactive charts and plots using Matplotlib and Seaborn
- **Statistical Analysis**: Comprehensive statistical tools powered by SciPy
- **Machine Learning**: Built-in ML capabilities using scikit-learn
- **Modern UI**: Dark theme with intuitive interface
- **Cross-Platform**: Runs on both Windows and macOS

## System Requirements

- **Windows**: Windows 10 or later
- **macOS**: macOS 10.14 (Mojave) or later
- **Python**: 3.8 or later (for development)

## Installation

### For End Users

#### Windows
1. Download the latest release from the releases page
2. Extract the ZIP file
3. Run `DataAnalysisApp.exe`

#### macOS
1. Download the latest release from the releases page
2. Open the DMG file
3. Drag `DataAnalysisApp.app` to your Applications folder
4. Run the application from Applications

### For Developers

1. Clone the repository:
```bash
git clone <repository-url>
cd Data-Analysis-Application
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python src/main.py
```

## Building from Source

### Windows

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the build script:
```bash
build_and_package.bat
```

3. The executable will be created in `dist/DataAnalysisApp/` and a ZIP package in `DataAnalysisApp-Windows-v1.0.0.zip`

### macOS

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

2. Make the build script executable and run it:
```bash
chmod +x build_mac.sh
./build_mac.sh
```

3. The application bundle will be created in `dist/DataAnalysisApp.app`

4. (Optional) Create a DMG installer:
```bash
hdiutil create -volname DataAnalysisApp -srcfolder dist/DataAnalysisApp.app -ov -format UDZO dist/DataAnalysisApp.dmg
```

## Project Structure

```
Data-Analysis-Application/
├── src/
│   ├── main.py              # Application entry point
│   └── ui/                  # UI components
│       ├── main_window.py   # Main application window
│       └── components/      # Reusable UI components
├── assets/                  # Application icons and resources
├── requirements.txt         # Python dependencies
├── data_analysis_app.spec   # PyInstaller configuration
├── build_and_package.bat    # Windows build and package script
├── build_mac.sh            # macOS build script
└── README.md               # This file
```

## Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Document functions and classes with docstrings

### Adding New Features
1. Create a new branch for your feature
2. Implement the feature in the appropriate module
3. Test thoroughly on both Windows and macOS if possible
4. Submit a pull request

## Dependencies

- **PyQt6**: Modern Qt6 bindings for Python
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **matplotlib**: Data visualization
- **seaborn**: Statistical data visualization
- **scipy**: Scientific computing
- **scikit-learn**: Machine learning
- **openpyxl**: Excel file support
- **PyInstaller**: Application packaging

## Troubleshooting

### Windows

**Issue**: Application doesn't start
- Make sure you have the Visual C++ Redistributable installed
- Try running as administrator

**Issue**: High DPI scaling issues
- The application should automatically handle high DPI displays
- If issues persist, try adjusting Windows display scaling settings

### macOS

**Issue**: "App is damaged and can't be opened"
- This is a Gatekeeper issue. Run: `xattr -cr /path/to/DataAnalysisApp.app`

**Issue**: Application won't open
- Right-click the app and select "Open" the first time
- Check System Preferences > Security & Privacy

## License

[Add your license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the GitHub repository.

## Version History

### Version 1.0.0
- Initial release
- Cross-platform support for Windows and macOS
- Modern dark theme UI
- Core data analysis features
