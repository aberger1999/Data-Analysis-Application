"""
Modern home screen for workspace selection and settings.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QGridLayout, QScrollArea,
    QDialog, QLineEdit, QMessageBox, QGroupBox,
    QComboBox, QCheckBox, QSpinBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
import os
import json
from datetime import datetime

class WorkspaceCard(QFrame):
    """Modern card widget for workspace selection."""

    clicked = pyqtSignal(int)
    deleted = pyqtSignal(int)
    renamed = pyqtSignal(int)

    def __init__(self, workspace_id, workspace_data, theme="dark"):
        super().__init__()
        self.workspace_id = workspace_id
        self.workspace_data = workspace_data
        self.current_theme = theme
        self.init_ui()

    def init_ui(self):
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(180)
        self.setMaximumWidth(300)
        self.update_theme()

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        top_layout = QHBoxLayout()

        icon_label = QLabel("📁")
        icon_label.setStyleSheet("font-size: 48px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(icon_label)

        top_layout.addStretch()

        rename_btn = QPushButton("✏️")
        rename_btn.setFixedSize(30, 30)
        rename_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a82da;
                border: none;
                border-radius: 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3b92ea;
            }
        """)
        rename_btn.clicked.connect(lambda: self.renamed.emit(self.workspace_id))
        top_layout.addWidget(rename_btn)

        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedSize(30, 30)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                border: none;
                border-radius: 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ef4444;
            }
        """)
        delete_btn.clicked.connect(lambda: self.deleted.emit(self.workspace_id))
        top_layout.addWidget(delete_btn)

        layout.addLayout(top_layout)

        name_label = QLabel(self.workspace_data.get('name', f'Workspace {self.workspace_id}'))
        name_font = QFont()
        name_font.setPointSize(14)
        name_font.setBold(True)
        name_label.setFont(name_font)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label)

        stats_text = (
            f"{self.workspace_data.get('file_count', 0)} files • "
            f"{self.workspace_data.get('graph_count', 0)} graphs • "
            f"{self.workspace_data.get('report_count', 0)} reports"
        )
        stats_label = QLabel(stats_text)
        stats_label.setStyleSheet("color: #aaaaaa; font-size: 10pt;")
        stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(stats_label)

        if self.workspace_data.get('last_modified'):
            date_label = QLabel(f"Modified: {self.workspace_data['last_modified']}")
            date_label.setStyleSheet("color: #888888; font-size: 9pt;")
            date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(date_label)

        layout.addStretch()

    def update_theme(self):
        is_dark = self.current_theme.lower() == "dark"

        if is_dark:
            self.setStyleSheet("""
                WorkspaceCard {
                    background-color: #2d2d2d;
                    border: 2px solid #555555;
                    border-radius: 12px;
                    padding: 20px;
                }
                WorkspaceCard:hover {
                    background-color: #3d3d3d;
                    border: 2px solid #2a82da;
                }
            """)
        else:
            self.setStyleSheet("""
                WorkspaceCard {
                    background-color: #ffffff;
                    border: 2px solid #cccccc;
                    border-radius: 12px;
                    padding: 20px;
                }
                WorkspaceCard:hover {
                    background-color: #f5f5f5;
                    border: 2px solid #2a82da;
                }
            """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.workspace_id)
        super().mousePressEvent(event)

class CreateWorkspaceCard(QFrame):
    """Card for creating a new workspace."""

    clicked = pyqtSignal()

    def __init__(self, theme="dark"):
        super().__init__()
        self.current_theme = theme
        self.init_ui()
        
    def init_ui(self):
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(180)
        self.setMaximumWidth(300)
        self.update_theme()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = QLabel("➕")
        icon_label.setStyleSheet("font-size: 64px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        text_label = QLabel("Create New Workspace")
        text_font = QFont()
        text_font.setPointSize(12)
        text_font.setBold(True)
        text_label.setFont(text_font)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(text_label)

    def update_theme(self):
        palette = self.palette()
        is_dark = self.current_theme.lower() == "dark"

        if is_dark:
            self.setStyleSheet("""
                CreateWorkspaceCard {
                    background-color: #1e1e1e;
                    border: 2px dashed #555555;
                    border-radius: 12px;
                    padding: 20px;
                }
                CreateWorkspaceCard:hover {
                    background-color: #2d2d2d;
                    border: 2px dashed #2a82da;
                }
            """)
        else:
            self.setStyleSheet("""
                CreateWorkspaceCard {
                    background-color: #fafafa;
                    border: 2px dashed #cccccc;
                    border-radius: 12px;
                    padding: 20px;
                }
                CreateWorkspaceCard:hover {
                    background-color: #f0f0f0;
                    border: 2px dashed #2a82da;
                }
            """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

class CreateWorkspaceDialog(QDialog):
    """Dialog for creating a new workspace."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.workspace_name = ""
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Create New Workspace")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        title_label = QLabel("Create New Workspace")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        desc_label = QLabel("Enter a name for your new workspace:")
        desc_label.setStyleSheet("color: #aaaaaa; margin-bottom: 10px;")
        layout.addWidget(desc_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Sales Analysis, Customer Data, etc.")
        self.name_input.setStyleSheet("padding: 8px; font-size: 11pt;")
        layout.addWidget(self.name_input)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        create_btn = QPushButton("Create Workspace")
        create_btn.setStyleSheet("background-color: #2a82da; font-weight: bold;")
        create_btn.clicked.connect(self.accept)
        button_layout.addWidget(create_btn)
        
        layout.addLayout(button_layout)
        
    def get_workspace_name(self):
        return self.name_input.text().strip()


class RenameWorkspaceDialog(QDialog):
    """Dialog for renaming a workspace."""

    def __init__(self, parent=None, current_name=""):
        super().__init__(parent)
        self.current_name = current_name
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Rename Workspace")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        title_label = QLabel("Rename Workspace")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        desc_label = QLabel("Enter a new name for your workspace:")
        desc_label.setStyleSheet("color: #aaaaaa; margin-bottom: 10px;")
        layout.addWidget(desc_label)

        self.name_input = QLineEdit()
        self.name_input.setText(self.current_name)
        self.name_input.setPlaceholderText("e.g., Sales Analysis, Customer Data, etc.")
        self.name_input.setStyleSheet("padding: 8px; font-size: 11pt;")
        self.name_input.selectAll()
        layout.addWidget(self.name_input)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        rename_btn = QPushButton("Rename")
        rename_btn.setStyleSheet("background-color: #2a82da; font-weight: bold;")
        rename_btn.clicked.connect(self.accept)
        button_layout.addWidget(rename_btn)

        layout.addLayout(button_layout)

    def get_workspace_name(self):
        return self.name_input.text().strip()


class SettingsDialog(QDialog):
    """Dialog for application settings."""
    
    theme_changed = pyqtSignal(str)
    
    def __init__(self, parent=None, current_theme="dark"):
        super().__init__(parent)
        self.current_theme = current_theme
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Settings")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        layout = QVBoxLayout(self)
        
        title_label = QLabel("⚙️ Settings")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        appearance_group = QGroupBox("Appearance")
        appearance_layout = QVBoxLayout(appearance_group)
        
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        theme_layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.setCurrentText(self.current_theme.capitalize())
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        
        appearance_layout.addLayout(theme_layout)
        layout.addWidget(appearance_group)
        
        data_group = QGroupBox("Data Settings")
        data_layout = QVBoxLayout(data_group)
        
        auto_save_layout = QHBoxLayout()
        self.auto_save_check = QCheckBox("Auto-save data on changes")
        self.auto_save_check.setChecked(True)
        auto_save_layout.addWidget(self.auto_save_check)
        data_layout.addLayout(auto_save_layout)
        
        decimal_layout = QHBoxLayout()
        decimal_label = QLabel("Decimal places:")
        decimal_layout.addWidget(decimal_label)
        
        self.decimal_spin = QSpinBox()
        self.decimal_spin.setRange(0, 10)
        self.decimal_spin.setValue(2)
        decimal_layout.addWidget(self.decimal_spin)
        decimal_layout.addStretch()
        
        data_layout.addLayout(decimal_layout)
        layout.addWidget(data_group)
        
        visualization_group = QGroupBox("Visualization Settings")
        viz_layout = QVBoxLayout(visualization_group)
        
        dpi_layout = QHBoxLayout()
        dpi_label = QLabel("Export DPI:")
        dpi_layout.addWidget(dpi_label)
        
        self.dpi_combo = QComboBox()
        self.dpi_combo.addItems(["150", "300", "600"])
        self.dpi_combo.setCurrentText("300")
        dpi_layout.addWidget(self.dpi_combo)
        dpi_layout.addStretch()
        
        viz_layout.addLayout(dpi_layout)
        layout.addWidget(visualization_group)
        
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("background-color: #2a82da; font-weight: bold; padding: 8px 20px;")
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
    def on_theme_changed(self, theme):
        self.theme_changed.emit(theme.lower())

class HomeScreen(QWidget):
    """Modern home screen with workspace selection."""

    workspace_selected = pyqtSignal(int, str)
    theme_changed = pyqtSignal(str)

    def __init__(self, initial_theme="light"):
        super().__init__()
        self.workspaces_dir = "workspaces"
        self.workspaces = []
        self.current_theme = initial_theme
        self.init_workspace_structure()
        self.init_ui()
        self.load_workspaces()

    def init_workspace_structure(self):
        """Initialize workspace directory structure."""
        if not os.path.exists(self.workspaces_dir):
            os.makedirs(self.workspaces_dir)

        workspace_1_path = os.path.join(self.workspaces_dir, "workspace_1")
        if not os.path.exists(workspace_1_path):
            self.create_workspace_structure(1, "My Workspace")

    def create_workspace_structure(self, workspace_id, name):
        """Create a new workspace structure."""
        workspace_path = os.path.join(self.workspaces_dir, f"workspace_{workspace_id}")

        if not os.path.exists(workspace_path):
            os.makedirs(workspace_path)
            os.makedirs(os.path.join(workspace_path, "data"))
            os.makedirs(os.path.join(workspace_path, "graphs"))
            os.makedirs(os.path.join(workspace_path, "reports"))

            metadata = {
                "id": workspace_id,
                "name": name,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "file_count": 0,
                "graph_count": 0,
                "report_count": 0
            }

            with open(os.path.join(workspace_path, "metadata.json"), 'w') as f:
                json.dump(metadata, f, indent=4)

    def _handle_remove_readonly(self, func, path, exc_info):
        import stat
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_label = QLabel("📊 Data Analysis Application")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_layout.addWidget(title_label)

        self.subtitle_label = QLabel("Select a workspace to begin your analysis")
        self.subtitle_label.setStyleSheet("color: #aaaaaa; font-size: 12pt;")
        title_layout.addWidget(self.subtitle_label)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        self.settings_btn = QPushButton("⚙️ Settings")
        self.settings_btn.clicked.connect(self.show_settings)
        header_layout.addWidget(self.settings_btn)

        layout.addLayout(header_layout)

        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setStyleSheet("background-color: #555555;")
        layout.addWidget(self.separator)

        workspaces_header_layout = QHBoxLayout()

        workspaces_label = QLabel("Your Workspaces")
        workspaces_font = QFont()
        workspaces_font.setPointSize(14)
        workspaces_font.setBold(True)
        workspaces_label.setFont(workspaces_font)
        workspaces_header_layout.addWidget(workspaces_label)

        workspaces_header_layout.addStretch()

        self.create_workspace_btn = QPushButton("➕ Create Workspace")
        self.create_workspace_btn.clicked.connect(self.create_new_workspace)
        workspaces_header_layout.addWidget(self.create_workspace_btn)

        layout.addLayout(workspaces_header_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")

        self.workspaces_container = QWidget()
        self.workspaces_layout = QGridLayout(self.workspaces_container)
        self.workspaces_layout.setSpacing(20)
        self.workspaces_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        scroll_area.setWidget(self.workspaces_container)
        layout.addWidget(scroll_area)

        self.update_home_theme()

    def update_home_theme(self):
        """Update theme for home screen elements."""
        is_dark = self.current_theme.lower() == "dark"

        if is_dark:
            self.subtitle_label.setStyleSheet("color: #aaaaaa; font-size: 12pt;")
            self.separator.setStyleSheet("background-color: #555555;")
            self.settings_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2d2d2d;
                    border: 1px solid #555555;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 11pt;
                }
                QPushButton:hover {
                    background-color: #3d3d3d;
                    border: 1px solid #2a82da;
                }
            """)
            self.create_workspace_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2a82da;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 11pt;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #3a92ea;
                }
            """)
        else:
            self.subtitle_label.setStyleSheet("color: #666666; font-size: 12pt;")
            self.separator.setStyleSheet("background-color: #cccccc;")
            self.settings_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e0e0e0;
                    border: 1px solid #aaaaaa;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 11pt;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                    border: 1px solid #2a82da;
                }
            """)
            self.create_workspace_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2a82da;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 11pt;
                    font-weight: bold;
                    color: #ffffff;
                }
                QPushButton:hover {
                    background-color: #3a92ea;
                }
            """)

    def load_workspaces(self):
        """Load and display all workspaces."""
        for i in reversed(range(self.workspaces_layout.count())):
            widget = self.workspaces_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.workspaces = []
        row, col = 0, 0

        if not os.path.exists(self.workspaces_dir):
            return

        workspace_dirs = [d for d in os.listdir(self.workspaces_dir)
                         if os.path.isdir(os.path.join(self.workspaces_dir, d))
                         and d.startswith("workspace_")]

        workspace_ids = []
        for d in workspace_dirs:
            try:
                workspace_id = int(d.split("_")[1])
                workspace_ids.append(workspace_id)
            except (ValueError, IndexError):
                continue

        workspace_ids.sort()

        for workspace_id in workspace_ids:
            workspace_path = os.path.join(self.workspaces_dir, f"workspace_{workspace_id}")
            metadata_path = os.path.join(workspace_path, "metadata.json")

            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)

                metadata['file_count'] = len([f for f in os.listdir(os.path.join(workspace_path, "data")) if os.path.isfile(os.path.join(workspace_path, "data", f))])
                metadata['graph_count'] = len([f for f in os.listdir(os.path.join(workspace_path, "graphs")) if f.endswith('.png')])
                metadata['report_count'] = len([f for f in os.listdir(os.path.join(workspace_path, "reports")) if f.endswith(('.html', '.pdf'))])

                self.workspaces.append(metadata)

                card = WorkspaceCard(workspace_id, metadata, self.current_theme)
                card.clicked.connect(self.on_workspace_clicked)
                card.deleted.connect(self.delete_workspace)
                card.renamed.connect(self.rename_workspace)

                self.workspaces_layout.addWidget(card, row, col)

                col += 1
                if col >= 3:
                    col = 0
                    row += 1

        if len(self.workspaces) == 0:
            empty_label = QLabel("No workspaces yet. Click 'Create Workspace' to get started!")
            empty_label.setStyleSheet("color: #aaaaaa; font-size: 12pt; padding: 40px;")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.workspaces_layout.addWidget(empty_label, 0, 0, 1, 3)

    def on_workspace_clicked(self, workspace_id):
        """Handle workspace selection."""
        workspace_path = os.path.join(self.workspaces_dir, f"workspace_{workspace_id}")
        metadata_path = os.path.join(workspace_path, "metadata.json")

        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        metadata['last_modified'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4)

        self.workspace_selected.emit(workspace_id, workspace_path)

    def create_new_workspace(self):
        """Create a new workspace."""
        dialog = CreateWorkspaceDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = dialog.get_workspace_name()
            if not name:
                name = f"Workspace {len(self.workspaces) + 1}"

            existing_ids = [w['id'] for w in self.workspaces]
            next_id = 1
            while next_id in existing_ids:
                next_id += 1

            self.create_workspace_structure(next_id, name)
            self.load_workspaces()

            QMessageBox.information(
                self,
                "Workspace Created",
                f"Workspace '{name}' has been created successfully!"
            )

    def rename_workspace(self, workspace_id):
        """Rename a workspace."""
        workspace_path = os.path.join(self.workspaces_dir, f"workspace_{workspace_id}")
        metadata_path = os.path.join(workspace_path, "metadata.json")

        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)

            current_name = metadata.get('name', f'Workspace {workspace_id}')

            dialog = RenameWorkspaceDialog(self, current_name)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_name = dialog.get_workspace_name()
                if new_name and new_name != current_name:
                    metadata['name'] = new_name
                    metadata['last_modified'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    with open(metadata_path, 'w') as f:
                        json.dump(metadata, f, indent=4)

                    self.load_workspaces()

                    QMessageBox.information(
                        self,
                        "Workspace Renamed",
                        f"Workspace renamed to '{new_name}'."
                    )

    def delete_workspace(self, workspace_id):
        """Delete a workspace."""
        workspace_path = os.path.join(self.workspaces_dir, f"workspace_{workspace_id}")
        metadata_path = os.path.join(workspace_path, "metadata.json")

        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)

            workspace_name = metadata.get('name', f'Workspace {workspace_id}')

            reply = QMessageBox.question(
                self,
                "Delete Workspace",
                f"Are you sure you want to delete '{workspace_name}'?\n\n"
                "This will permanently remove all data, graphs, and reports in this workspace.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                import shutil
                try:
                    shutil.rmtree(workspace_path, onerror=self._handle_remove_readonly)
                    self.load_workspaces()

                    QMessageBox.information(
                        self,
                        "Workspace Deleted",
                        f"Workspace '{workspace_name}' has been deleted."
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Delete Failed",
                        f"Failed to delete workspace: {str(e)}"
                    )
    
    def show_settings(self):
        """Show settings dialog."""
        dialog = SettingsDialog(self, self.current_theme)
        dialog.theme_changed.connect(self.on_theme_changed)
        dialog.exec()

    def on_theme_changed(self, theme):
        """Handle theme change."""
        self.current_theme = theme.lower()
        self.theme_changed.emit(theme.lower())
        self.update_home_theme()
        self.update_all_themes()

    def update_all_themes(self):
        """Update theme for all workspace cards."""
        for i in range(self.workspaces_layout.count()):
            widget = self.workspaces_layout.itemAt(i).widget()
            if widget and hasattr(widget, 'update_theme'):
                if hasattr(widget, 'current_theme'):
                    widget.current_theme = self.current_theme
                widget.update_theme()
