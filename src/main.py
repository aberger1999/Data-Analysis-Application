"""
Main entry point for the Data Analysis Application.
This module initializes the PyQt5 application and launches the main window.
Cross-platform support for Windows and macOS.
"""

import sys
import os
import warnings
import platform

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QLibraryInfo, Qt
from PyQt5.QtGui import QPalette, QColor, QIcon
from ui.main_window import MainWindow

if platform.system() == 'Darwin':
    warnings.filterwarnings("ignore", ".*overrides the method identifier.*")
    warnings.filterwarnings("ignore", ".*chose.*")

def set_dark_theme(app):
    """Set a modern dark theme for the application."""
    # Set the fusion style as a base
    app.setStyle('Fusion')
    
    # Create a custom dark palette
    palette = QPalette()
    
    # Set colors
    dark_color = QColor(45, 45, 45)
    disabled_color = QColor(127, 127, 127)
    text_color = QColor(255, 255, 255)
    highlight_color = QColor(42, 130, 218)
    highlight_text_color = QColor(255, 255, 255)
    
    # Base colors
    palette.setColor(QPalette.ColorRole.Window, dark_color)
    palette.setColor(QPalette.ColorRole.WindowText, text_color)
    palette.setColor(QPalette.ColorRole.Base, QColor(18, 18, 18))
    palette.setColor(QPalette.ColorRole.AlternateBase, dark_color)
    palette.setColor(QPalette.ColorRole.ToolTipBase, dark_color)
    palette.setColor(QPalette.ColorRole.ToolTipText, text_color)
    palette.setColor(QPalette.ColorRole.Text, text_color)
    palette.setColor(QPalette.ColorRole.PlaceholderText, disabled_color)
    
    # Button colors
    palette.setColor(QPalette.ColorRole.Button, dark_color)
    palette.setColor(QPalette.ColorRole.ButtonText, text_color)
    
    # Highlight colors
    palette.setColor(QPalette.ColorRole.Highlight, highlight_color)
    palette.setColor(QPalette.ColorRole.HighlightedText, highlight_text_color)
    
    # Link colors
    palette.setColor(QPalette.ColorRole.Link, highlight_color)
    palette.setColor(QPalette.ColorRole.LinkVisited, highlight_color.lighter())
    
    # Apply the palette
    app.setPalette(palette)
    
    # Additional stylesheet for fine-tuning
    app.setStyleSheet("""
        QWidget {
            font-size: 10pt;
        }
        
        QTableView {
            gridline-color: #3d3d3d;
            selection-background-color: #2a82da;
            selection-color: #ffffff;
            alternate-background-color: #353535;
        }
        
        QTableView::item:selected {
            background-color: #2a82da;
        }
        
        QHeaderView::section {
            background-color: #2d2d2d;
            color: #ffffff;
            padding: 5px;
            border: 1px solid #3d3d3d;
        }
        
        QPushButton {
            background-color: #2d2d2d;
            color: #ffffff;
            border: 1px solid #555555;
            padding: 5px 10px;
            border-radius: 3px;
        }
        
        QPushButton:hover {
            background-color: #3d3d3d;
        }
        
        QPushButton:pressed {
            background-color: #2a82da;
        }
        
        QPushButton:disabled {
            background-color: #1e1e1e;
            color: #7f7f7f;
            border: 1px solid #3d3d3d;
        }
        
        QComboBox {
            background-color: #2d2d2d;
            color: #ffffff;
            border: 1px solid #555555;
            padding: 3px;
            border-radius: 3px;
        }
        
        QComboBox:hover {
            background-color: #3d3d3d;
        }
        
        QComboBox QAbstractItemView {
            background-color: #2d2d2d;
            color: #ffffff;
            selection-background-color: #2a82da;
        }
        
        QLineEdit {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #555555;
            padding: 3px;
            border-radius: 3px;
        }
        
        QTabWidget::pane {
            border: 1px solid #3d3d3d;
        }
        
        QTabBar::tab {
            background-color: #2d2d2d;
            color: #ffffff;
            padding: 8px 12px;
            border: 1px solid #3d3d3d;
            border-bottom: none;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected {
            background-color: #2a82da;
        }
        
        QTabBar::tab:!selected {
            margin-top: 2px;
        }
        
        QGroupBox {
            border: 1px solid #3d3d3d;
            border-radius: 5px;
            margin-top: 1ex;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 5px;
            color: #ffffff;
        }
        
        QScrollBar:vertical {
            border: none;
            background-color: #2d2d2d;
            width: 10px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #555555;
            min-height: 20px;
            border-radius: 5px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #2a82da;
        }
        
        QScrollBar:horizontal {
            border: none;
            background-color: #2d2d2d;
            height: 10px;
            margin: 0px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #555555;
            min-width: 20px;
            border-radius: 5px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #2a82da;
        }
        
        QScrollBar::add-line, QScrollBar::sub-line {
            border: none;
            background: none;
        }
        
        QScrollBar::add-page, QScrollBar::sub-page {
            background: none;
        }
    """)

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and PyInstaller.
    
    Args:
        relative_path: Path relative to the project root
        
    Returns:
        Absolute path to the resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Development mode - use the project root directory
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, relative_path)

def main():
    """Initialize and run the application."""
    if platform.system() == 'Windows':
        try:
            from ctypes import windll
            windll.shell32.SetCurrentProcessExplicitAppUserModelID('com.dataanalysis.app')
        except:
            pass

        # Fix DLL loading issue with Anaconda Python
        # Prioritize virtual environment's DLLs over Anaconda's base environment
        venv_scripts = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'venv', 'Scripts')
        if os.path.exists(venv_scripts):
            current_path = os.environ.get('PATH', '')
            if venv_scripts not in current_path:
                os.environ['PATH'] = venv_scripts + os.pathsep + current_path

    plugins_path = QLibraryInfo.location(QLibraryInfo.PluginsPath)
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugins_path

    app = QApplication(sys.argv)
    app.setApplicationName("Data Analysis Application")
    app.setOrganizationName("DataAnalysis")
    app.setOrganizationDomain("dataanalysis.app")

    icon_path = resource_path('icon.png')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Set Fusion style for consistent look
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main() 