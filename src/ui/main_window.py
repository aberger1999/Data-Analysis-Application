"""
Main window for the Data Analysis Application.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QApplication, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon
from .components.home_screen import HomeScreen
from .components.workspace_view import WorkspaceView
import json
import os
import sys

class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.current_theme = "dark"
        self.init_ui()
        self.setup_connections()
        
    def _resource_path(self, relative_path):
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
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        return os.path.join(base_path, relative_path)
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Data Analysis Application")
        self.setMinimumSize(1200, 800)
        
        # Set window icon (works in both dev and packaged mode)
        icon_path = self._resource_path('icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create stacked widget for home screen and workspace view
        self.stacked_widget = QStackedWidget()

        # Initialize with light theme first
        self.current_theme = "light"

        self.home_screen = HomeScreen(initial_theme="light")
        self.stacked_widget.addWidget(self.home_screen)

        self.workspace_view = WorkspaceView()
        self.stacked_widget.addWidget(self.workspace_view)

        layout.addWidget(self.stacked_widget)

        # Apply light theme to main window
        self.set_light_theme()
        self.workspace_view.update_theme("light")

    def setup_connections(self):
        """Setup signal connections."""
        self.home_screen.workspace_selected.connect(self.open_workspace)
        self.home_screen.theme_changed.connect(self.change_theme)
        self.workspace_view.back_to_home.connect(self.show_home_screen)

    def open_workspace(self, workspace_id, workspace_path):
        """Open a workspace."""
        metadata_path = os.path.join(workspace_path, "metadata.json")

        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        workspace_name = metadata.get('name', f'Workspace {workspace_id}')

        self.workspace_view.set_workspace(workspace_id, workspace_path, workspace_name)
        self.stacked_widget.setCurrentWidget(self.workspace_view)

    def show_home_screen(self):
        """Return to home screen."""
        self.home_screen.load_workspaces()
        self.stacked_widget.setCurrentWidget(self.home_screen)

    def change_theme(self, theme):
        """Change application theme."""
        self.current_theme = theme
        if theme == "light":
            self.set_light_theme()
        else:
            self.set_dark_theme()

        # Update other components
        self.workspace_view.update_theme(theme)

    def set_light_theme(self):
        """Set light theme."""
        palette = QPalette()

        light_color = QColor(240, 240, 240)
        text_color = QColor(0, 0, 0)
        highlight_color = QColor(42, 130, 218)

        palette.setColor(QPalette.ColorRole.Window, light_color)
        palette.setColor(QPalette.ColorRole.WindowText, text_color)
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.AlternateBase, light_color)
        palette.setColor(QPalette.ColorRole.ToolTipBase, light_color)
        palette.setColor(QPalette.ColorRole.ToolTipText, text_color)
        palette.setColor(QPalette.ColorRole.Text, text_color)
        palette.setColor(QPalette.ColorRole.Button, light_color)
        palette.setColor(QPalette.ColorRole.ButtonText, text_color)
        palette.setColor(QPalette.ColorRole.Highlight, highlight_color)
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

        app = QApplication.instance()
        app.setPalette(palette)

        app.setStyleSheet("""
            QWidget {
                font-size: 10pt;
            }
            QTableView {
                gridline-color: #cccccc;
                selection-background-color: #2a82da;
                selection-color: #ffffff;
                alternate-background-color: #f5f5f5;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                color: #000000;
                padding: 5px;
                border: 1px solid #cccccc;
            }
            QPushButton {
                background-color: #e0e0e0;
                color: #000000;
                border: 1px solid #aaaaaa;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #2a82da;
                color: #ffffff;
            }
        """)

    def set_dark_theme(self):
        """Set dark theme."""
        palette = QPalette()

        dark_color = QColor(45, 45, 45)
        text_color = QColor(255, 255, 255)
        highlight_color = QColor(42, 130, 218)

        palette.setColor(QPalette.ColorRole.Window, dark_color)
        palette.setColor(QPalette.ColorRole.WindowText, text_color)
        palette.setColor(QPalette.ColorRole.Base, QColor(18, 18, 18))
        palette.setColor(QPalette.ColorRole.AlternateBase, dark_color)
        palette.setColor(QPalette.ColorRole.ToolTipBase, dark_color)
        palette.setColor(QPalette.ColorRole.ToolTipText, text_color)
        palette.setColor(QPalette.ColorRole.Text, text_color)
        palette.setColor(QPalette.ColorRole.Button, dark_color)
        palette.setColor(QPalette.ColorRole.ButtonText, text_color)
        palette.setColor(QPalette.ColorRole.Highlight, highlight_color)
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

        app = QApplication.instance()
        app.setPalette(palette)

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
        """)

    def show_error(self, message):
        """Show error message dialog."""
        QMessageBox.critical(self, "Error", message)

    def closeEvent(self, event):
        """Handle window close event with unsaved changes check."""
        if self.stacked_widget.currentWidget() == self.workspace_view:
            if self.workspace_view.has_unsaved_changes:
                reply = QMessageBox.question(
                    self,
                    "Unsaved Changes",
                    "You have unsaved changes. Do you want to save before exiting?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
                )

                if reply == QMessageBox.StandardButton.Cancel:
                    event.ignore()
                    return
                elif reply == QMessageBox.StandardButton.Yes:
                    self.workspace_view.save_workspace()

        event.accept() 