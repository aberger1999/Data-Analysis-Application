"""
Workspace view containing all data analysis tools.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QSplitter, QTabWidget, QFileDialog,
    QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import os
from .data_preview import DataPreviewPanel
from .analysis_panel import AnalysisPanel
from .visualization_panel import VisualizationPanel
from .preprocessing_panel import PreprocessingPanel
from .feature_engineering_panel import FeatureEngineeringPanel
from .machine_learning_panel import MachineLearningPanel
from .report_generator_panel import ReportGeneratorPanel
from .dataset_manager_panel import DatasetManagerDialog
from ..data_manager import DataManager

class WorkspaceView(QWidget):
    """View for working within a specific workspace."""
    
    back_to_home = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.workspace_id = None
        self.workspace_path = None
        self.workspace_name = ""
        self.has_unsaved_changes = False
        self.dataset_manager_dialog = None
        self.init_ui()
        self.setup_connections()

    def update_theme(self, theme_name):
        is_dark = theme_name.lower() == "dark"

        # Colors
        bg_color = "#1e1e1e" if is_dark else "#f0f0f0"
        text_color = "#ffffff" if is_dark else "#000000"
        border_color = "#3d3d3d" if is_dark else "#cccccc"
        btn_bg = "#2d2d2d" if is_dark else "#e0e0e0"
        btn_hover = "#3d3d3d" if is_dark else "#d0d0d0"

        # Header style
        self.header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-bottom: 2px solid #2a82da;
            }}
        """)

        # Back button style
        self.back_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {btn_bg};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 10pt;
            }}
            QPushButton:hover {{
                background-color: {btn_hover};
                border: 1px solid #2a82da;
            }}
        """)

        # Save button style
        self.save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {btn_bg};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 10pt;
            }}
            QPushButton:hover:enabled {{
                background-color: {btn_hover};
                border: 1px solid #2a82da;
            }}
            QPushButton:disabled {{
                background-color: {bg_color};
                color: #7f7f7f;
            }}
        """)

        # Tabs style
        tab_bg = "#2d2d2d" if is_dark else "#e0e0e0"
        tab_selected = "#2a82da"
        tab_text_selected = "#ffffff"

        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {border_color};
                border-radius: 4px;
            }}
            QTabBar::tab {{
                background-color: {tab_bg};
                color: {text_color};
                padding: 10px 16px;
                border: 1px solid {border_color};
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background-color: {tab_selected};
                color: {tab_text_selected};
            }}
            QTabBar::tab:!selected {{
                margin-top: 2px;
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {btn_hover};
            }}
        """)

        # Update child panels
        if hasattr(self, 'analysis_panel'):
            self.analysis_panel.update_theme(theme_name)

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.header_frame = QFrame()
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)

        self.back_btn = QPushButton("← Back to Home")
        self.back_btn.clicked.connect(self.on_back_clicked)
        header_layout.addWidget(self.back_btn)

        header_layout.addSpacing(20)

        self.workspace_label = QLabel()
        workspace_font = QFont()
        workspace_font.setPointSize(14)
        workspace_font.setBold(True)
        self.workspace_label.setFont(workspace_font)
        header_layout.addWidget(self.workspace_label)

        header_layout.addStretch()

        self.dataset_manager_btn = QPushButton("📊 Dataset Manager")
        self.dataset_manager_btn.setStyleSheet("""
            QPushButton {
                background-color: #4d4d4d;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 10pt;
                color: white;
            }
            QPushButton:hover {
                background-color: #5d5d5d;
            }
        """)
        self.dataset_manager_btn.clicked.connect(self.show_dataset_manager)
        header_layout.addWidget(self.dataset_manager_btn)

        self.load_btn = QPushButton("📂 Import CSV")
        self.load_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a82da;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 10pt;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #3a92ea;
            }
        """)
        self.load_btn.clicked.connect(self.load_data)
        header_layout.addWidget(self.load_btn)

        self.save_btn = QPushButton("💾 Save Workspace")
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_workspace)
        header_layout.addWidget(self.save_btn)

        self.export_btn = QPushButton("📤 Export CSV")
        self.export_btn.setEnabled(False)
        self.export_btn.clicked.connect(self.save_data)
        header_layout.addWidget(self.export_btn)

        layout.addWidget(self.header_frame)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(10, 10, 10, 10)

        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        self.data_preview = DataPreviewPanel(self.data_manager)
        main_splitter.addWidget(self.data_preview)

        self.tabs = QTabWidget()

        self.preprocessing_panel = PreprocessingPanel(self.data_manager)

        # Apply initial theme (will be updated by MainWindow)
        self.update_theme("dark")
        self.tabs.addTab(self.preprocessing_panel, "🔧 Preprocessing")

        self.analysis_panel = AnalysisPanel(self.data_manager)
        self.tabs.addTab(self.analysis_panel, "📊 Analysis")

        self.visualization_panel = VisualizationPanel(self.data_manager)
        self.tabs.addTab(self.visualization_panel, "📈 Visualization")

        self.feature_engineering_panel = FeatureEngineeringPanel(self.data_manager)
        self.tabs.addTab(self.feature_engineering_panel, "⚙️ Feature Engineering")

        self.machine_learning_panel = MachineLearningPanel(self.data_manager)
        self.tabs.addTab(self.machine_learning_panel, "🤖 Machine Learning")

        self.report_generator_panel = ReportGeneratorPanel(self.data_manager)
        self.tabs.addTab(self.report_generator_panel, "📄 Reports")

        main_splitter.addWidget(self.tabs)
        main_splitter.setSizes([400, 800])

        content_layout.addWidget(main_splitter)
        layout.addLayout(content_layout)
        
    def setup_connections(self):
        """Setup signal connections."""
        self.data_manager.data_error.connect(self.show_error)
        self.data_manager.data_loaded.connect(self.on_data_loaded)

        self.preprocessing_panel.data_modified.connect(self.mark_unsaved_changes)
        self.feature_engineering_panel.data_modified.connect(self.mark_unsaved_changes)

        self.back_btn.clicked.disconnect()
        self.back_btn.clicked.connect(self.on_back_clicked)

    def set_workspace(self, workspace_id, workspace_path, workspace_name):
        """Set the active workspace."""
        self.workspace_id = workspace_id
        self.workspace_path = workspace_path
        self.workspace_name = workspace_name
        self.has_unsaved_changes = False

        self.workspace_label.setText(f"📁 {workspace_name}")

        # Clear existing data from previous workspace
        self.data_manager.clear_data()

        self.data_manager.set_workspace_path(workspace_path)
        self.visualization_panel.set_workspace_path(workspace_path)
        self.report_generator_panel.set_workspace_path(workspace_path)

        # Try to load existing workspace data
        self.data_manager.load_workspace_data()
        
    def load_data(self):
        """Load data from file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Data File",
            "",
            "Data Files (*.csv *.xlsx *.xls);;CSV Files (*.csv);;Excel Files (*.xlsx *.xls)"
        )
        
        if file_path:
            if file_path.endswith('.csv'):
                self.data_manager.load_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                self.data_manager.load_excel(file_path)
                
    def save_data(self):
        """Save current data."""
        if self.data_manager.data is None:
            return
            
        default_path = ""
        if self.workspace_path:
            default_path = os.path.join(self.workspace_path, "data", "data.csv")
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Data File",
            default_path,
            "CSV Files (*.csv);;Excel Files (*.xlsx)"
        )
        
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.data_manager.data.to_csv(file_path, index=False)
                elif file_path.endswith('.xlsx'):
                    self.data_manager.data.to_excel(file_path, index=False)
                    
                QMessageBox.information(
                    self,
                    "Success",
                    f"Data saved successfully to {file_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Error saving data: {str(e)}"
                )
    
    def load_dataset_from_manager(self, file_path):
        """Load a dataset selected from the dataset manager."""
        if self.has_unsaved_changes:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before loading a new dataset?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )

            if reply == QMessageBox.StandardButton.Cancel:
                return
            elif reply == QMessageBox.StandardButton.Yes:
                self.save_workspace()

        self.data_manager.load_csv(file_path)
        self.has_unsaved_changes = False
        self.update_save_button()

        if self.dataset_manager_dialog:
            filename = os.path.basename(file_path)
            self.dataset_manager_dialog.set_current_dataset(filename)

    def on_dataset_deleted(self, filename):
        """Handle dataset deletion."""
        if self.data_manager.data is not None:
            current_file = os.path.join(self.workspace_path, "data", "workspace_data.csv")
            if os.path.exists(current_file):
                self.data_manager.load_workspace_data()

    def on_dataset_renamed(self, old_name, new_name):
        """Handle dataset rename."""
        pass

    def show_dataset_manager(self):
        """Show the dataset manager dialog."""
        if not self.dataset_manager_dialog:
            self.dataset_manager_dialog = DatasetManagerDialog(self)
            self.dataset_manager_dialog.dataset_selected.connect(self.load_dataset_from_manager)
            self.dataset_manager_dialog.dataset_deleted.connect(self.on_dataset_deleted)
            self.dataset_manager_dialog.dataset_renamed.connect(self.on_dataset_renamed)

        self.dataset_manager_dialog.set_workspace(self.workspace_path)
        self.dataset_manager_dialog.exec()

    def mark_unsaved_changes(self):
        """Mark that there are unsaved changes."""
        self.has_unsaved_changes = True
        self.update_save_button()

    def update_save_button(self):
        """Update the save button state."""
        has_data = self.data_manager.data is not None
        self.save_btn.setEnabled(has_data)
        self.export_btn.setEnabled(has_data)

        if self.has_unsaved_changes and has_data:
            self.save_btn.setText("💾 Save Workspace *")
            self.save_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f59e0b;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-size: 10pt;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #d97706;
                }
            """)
        else:
            self.save_btn.setText("💾 Save Workspace")
            self.save_btn.setStyleSheet("")

    def save_workspace(self):
        """Save the current workspace data."""
        if self.data_manager.data is None:
            return

        try:
            self.data_manager.save_workspace_data()
            self.has_unsaved_changes = False
            self.update_save_button()

            if self.dataset_manager_dialog:
                self.dataset_manager_dialog.set_current_dataset("workspace_data.csv")

            QMessageBox.information(
                self,
                "Success",
                "Workspace data saved successfully!"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error saving workspace: {str(e)}"
            )

    def on_back_clicked(self):
        """Handle back button click with unsaved changes check."""
        if self.has_unsaved_changes:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before leaving?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )

            if reply == QMessageBox.StandardButton.Cancel:
                return
            elif reply == QMessageBox.StandardButton.Yes:
                self.save_workspace()

        self.back_to_home.emit()

    def on_data_loaded(self, df):
        """Handle when data is loaded."""
        self.update_save_button()
        if self.dataset_manager_dialog:
            self.dataset_manager_dialog.refresh_dataset_list()

    def show_error(self, message):
        """Show error message."""
        QMessageBox.critical(self, "Error", message)
