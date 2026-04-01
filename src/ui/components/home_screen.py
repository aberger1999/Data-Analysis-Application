"""
Modern home screen for workspace selection and settings.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QGridLayout, QScrollArea,
    QDialog, QLineEdit, QGroupBox,
    QComboBox, QCheckBox, QSpinBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from ..theme import get_colors, RADIUS_LG, RADIUS_MD, RADIUS_SM
from . import modal
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
        c = get_colors(self.current_theme)

        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(140)
        self.setMaximumHeight(160)
        self.setMaximumWidth(320)
        self.update_theme()

        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(14, 12, 14, 12)

        # Top row: icon + action buttons
        top_layout = QHBoxLayout()
        top_layout.setSpacing(6)

        icon_label = QLabel("📁")
        icon_label.setStyleSheet("font-size: 28px; background: transparent;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(icon_label)

        top_layout.addStretch()

        rename_btn = QPushButton("✏️")
        rename_btn.setFixedSize(22, 22)
        rename_btn.setToolTip("Rename workspace")
        rename_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['accent']};
                border: none;
                border-radius: 11px;
                font-size: 11px;
                padding: 0px;
                min-height: 0px;
            }}
            QPushButton:hover {{
                background-color: {c['accent_hover']};
            }}
        """)
        rename_btn.clicked.connect(lambda: self.renamed.emit(self.workspace_id))
        top_layout.addWidget(rename_btn)

        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedSize(22, 22)
        delete_btn.setToolTip("Delete workspace")
        delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['danger']};
                border: none;
                border-radius: 11px;
                font-size: 11px;
                padding: 0px;
                min-height: 0px;
            }}
            QPushButton:hover {{
                background-color: {c['danger_hover']};
            }}
        """)
        delete_btn.clicked.connect(lambda: self.deleted.emit(self.workspace_id))
        top_layout.addWidget(delete_btn)

        layout.addLayout(top_layout)

        # Workspace name
        name_label = QLabel(self.workspace_data.get('name', f'Workspace {self.workspace_id}'))
        name_font = QFont()
        name_font.setPointSize(10)
        name_font.setBold(True)
        name_label.setFont(name_font)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("background: transparent;")
        layout.addWidget(name_label)

        # Stats
        stats_text = (
            f"{self.workspace_data.get('file_count', 0)} files  ·  "
            f"{self.workspace_data.get('graph_count', 0)} graphs  ·  "
            f"{self.workspace_data.get('report_count', 0)} reports"
        )
        stats_label = QLabel(stats_text)
        stats_label.setStyleSheet(f"color: {c['text_secondary']}; font-size: 11px; background: transparent;")
        stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(stats_label)

        if self.workspace_data.get('last_modified'):
            date_label = QLabel(f"Modified: {self.workspace_data['last_modified']}")
            date_label.setStyleSheet(f"color: {c['text_disabled']}; font-size: 11px; background: transparent;")
            date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(date_label)

        layout.addStretch()

    def update_theme(self):
        c = get_colors(self.current_theme)
        self.setStyleSheet(f"""
            WorkspaceCard {{
                background-color: {c['bg_secondary']};
                border: 1px solid {c['border']};
                border-radius: {RADIUS_LG};
                padding: 14px;
            }}
            WorkspaceCard:hover {{
                background-color: {c['bg_tertiary']};
                border: 1px solid {c['accent']};
            }}
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
        c = get_colors(self.current_theme)

        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(140)
        self.setMaximumHeight(160)
        self.setMaximumWidth(320)
        self.update_theme()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(14, 12, 14, 12)

        icon_label = QLabel("➕")
        icon_label.setStyleSheet("font-size: 36px; background: transparent;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        text_label = QLabel("Create New Workspace")
        text_font = QFont()
        text_font.setPointSize(10)
        text_font.setBold(True)
        text_label.setFont(text_font)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setStyleSheet("background: transparent;")
        layout.addWidget(text_label)

    def update_theme(self):
        c = get_colors(self.current_theme)
        self.setStyleSheet(f"""
            CreateWorkspaceCard {{
                background-color: {c['bg_primary']};
                border: 2px dashed {c['border_medium']};
                border-radius: {RADIUS_LG};
                padding: 14px;
            }}
            CreateWorkspaceCard:hover {{
                background-color: {c['bg_secondary']};
                border: 2px dashed {c['accent']};
            }}
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

class CreateWorkspaceDialog(QDialog):
    """Dialog for creating a new workspace."""

    def __init__(self, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint)
        self.workspace_name = ""
        self.setModal(True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()

    def init_ui(self):
        c = get_colors("dark")

        # Overlay
        self._overlay = QWidget(self)
        self._overlay.setStyleSheet("background: rgba(0, 0, 0, 0.6);")

        # Box
        self._box = QWidget(self._overlay)
        self._box.setStyleSheet(f"""
            QWidget {{
                background-color: #1e2433;
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 10px;
            }}
        """)
        box_layout = QVBoxLayout(self._box)
        box_layout.setContentsMargins(24, 24, 24, 24)
        box_layout.setSpacing(16)

        title_label = QLabel("Create New Workspace")
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {c['text_primary']};
                font-size: 15px;
                font-weight: 700;
                background: transparent;
                border: none;
            }}
        """)
        box_layout.addWidget(title_label)

        desc_label = QLabel("Enter a name for your new workspace:")
        desc_label.setStyleSheet(f"""
            QLabel {{
                color: #9ca3af;
                font-size: 13px;
                background: transparent;
                border: none;
            }}
        """)
        box_layout.addWidget(desc_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Sales Analysis, Customer Data, etc.")
        self.name_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {c['bg_input']};
                color: {c['text_primary']};
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                min-height: 20px;
            }}
            QLineEdit:focus {{
                border-color: {c['accent']};
            }}
        """)
        box_layout.addWidget(self.name_input)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {c['text_secondary']};
                border: 1px solid {c['border']};
                border-radius: 6px;
                padding: 8px 20px;
                font-size: 12px;
                font-weight: 600;
                min-height: 0px;
            }}
            QPushButton:hover {{
                background-color: {c['bg_hover']};
                color: {c['text_primary']};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        create_btn = QPushButton("Create Workspace")
        create_btn.setCursor(Qt.PointingHandCursor)
        create_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['accent']};
                color: {c['text_inverse']};
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-size: 12px;
                font-weight: 600;
                min-height: 0px;
            }}
            QPushButton:hover {{
                background-color: {c['accent_hover']};
            }}
        """)
        create_btn.clicked.connect(self.accept)
        btn_layout.addWidget(create_btn)

        box_layout.addLayout(btn_layout)

        self.name_input.returnPressed.connect(self.accept)

    def _layout_children(self):
        if self.parent():
            self.resize(self.parent().size())
            self.move(self.parent().mapToGlobal(self.parent().rect().topLeft()))
        self._overlay.setGeometry(0, 0, self.width(), self.height())
        box_w = min(440, self.width() - 60)
        self._box.setFixedWidth(box_w)
        self._box.adjustSize()
        bx = (self.width() - box_w) // 2
        by = (self.height() - self._box.height()) // 2
        self._box.move(bx, by)

    def showEvent(self, event):
        super().showEvent(event)
        self._layout_children()
        self.name_input.setFocus()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._layout_children()

    def get_workspace_name(self):
        return self.name_input.text().strip()


class RenameWorkspaceDialog(QDialog):
    """Dialog for renaming a workspace."""

    def __init__(self, parent=None, current_name=""):
        super().__init__(parent, Qt.FramelessWindowHint)
        self.current_name = current_name
        self.setModal(True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()

    def init_ui(self):
        c = get_colors("dark")

        self._overlay = QWidget(self)
        self._overlay.setStyleSheet("background: rgba(0, 0, 0, 0.6);")

        self._box = QWidget(self._overlay)
        self._box.setStyleSheet(f"""
            QWidget {{
                background-color: #1e2433;
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 10px;
            }}
        """)
        box_layout = QVBoxLayout(self._box)
        box_layout.setContentsMargins(24, 24, 24, 24)
        box_layout.setSpacing(16)

        title_label = QLabel("Rename Workspace")
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {c['text_primary']};
                font-size: 15px;
                font-weight: 700;
                background: transparent;
                border: none;
            }}
        """)
        box_layout.addWidget(title_label)

        desc_label = QLabel("Enter a new name for your workspace:")
        desc_label.setStyleSheet(f"""
            QLabel {{
                color: #9ca3af;
                font-size: 13px;
                background: transparent;
                border: none;
            }}
        """)
        box_layout.addWidget(desc_label)

        self.name_input = QLineEdit()
        self.name_input.setText(self.current_name)
        self.name_input.setPlaceholderText("e.g., Sales Analysis, Customer Data, etc.")
        self.name_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {c['bg_input']};
                color: {c['text_primary']};
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                min-height: 20px;
            }}
            QLineEdit:focus {{
                border-color: {c['accent']};
            }}
        """)
        box_layout.addWidget(self.name_input)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {c['text_secondary']};
                border: 1px solid {c['border']};
                border-radius: 6px;
                padding: 8px 20px;
                font-size: 12px;
                font-weight: 600;
                min-height: 0px;
            }}
            QPushButton:hover {{
                background-color: {c['bg_hover']};
                color: {c['text_primary']};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        rename_btn = QPushButton("Rename")
        rename_btn.setCursor(Qt.PointingHandCursor)
        rename_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['accent']};
                color: {c['text_inverse']};
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-size: 12px;
                font-weight: 600;
                min-height: 0px;
            }}
            QPushButton:hover {{
                background-color: {c['accent_hover']};
            }}
        """)
        rename_btn.clicked.connect(self.accept)
        btn_layout.addWidget(rename_btn)

        box_layout.addLayout(btn_layout)

        self.name_input.returnPressed.connect(self.accept)

    def _layout_children(self):
        if self.parent():
            self.resize(self.parent().size())
            self.move(self.parent().mapToGlobal(self.parent().rect().topLeft()))
        self._overlay.setGeometry(0, 0, self.width(), self.height())
        box_w = min(440, self.width() - 60)
        self._box.setFixedWidth(box_w)
        self._box.adjustSize()
        bx = (self.width() - box_w) // 2
        by = (self.height() - self._box.height()) // 2
        self._box.move(bx, by)

    def showEvent(self, event):
        super().showEvent(event)
        self._layout_children()
        self.name_input.setFocus()
        self.name_input.selectAll()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._layout_children()

    def get_workspace_name(self):
        return self.name_input.text().strip()


class SettingsDialog(QDialog):
    """Dialog for application settings."""

    theme_changed = pyqtSignal(str)

    def __init__(self, parent=None, current_theme="dark"):
        super().__init__(parent, Qt.FramelessWindowHint)
        self.current_theme = current_theme
        self.setModal(True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()

    def init_ui(self):
        c = get_colors("dark")

        self._overlay = QWidget(self)
        self._overlay.setStyleSheet("background: rgba(0, 0, 0, 0.6);")

        self._box = QWidget(self._overlay)
        self._box.setStyleSheet(f"""
            QWidget {{
                background-color: #1e2433;
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 10px;
            }}
        """)
        box_layout = QVBoxLayout(self._box)
        box_layout.setContentsMargins(24, 24, 24, 24)
        box_layout.setSpacing(16)

        title_label = QLabel("Settings")
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {c['text_primary']};
                font-size: 16px;
                font-weight: 700;
                background: transparent;
                border: none;
            }}
        """)
        box_layout.addWidget(title_label)

        # ─ Appearance
        section_lbl = QLabel("APPEARANCE")
        section_lbl.setStyleSheet(f"""
            QLabel {{
                color: {c['accent']};
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1.2px;
                background: transparent;
                border: none;
            }}
        """)
        box_layout.addWidget(section_lbl)

        theme_row = QHBoxLayout()
        theme_lbl = QLabel("Theme:")
        theme_lbl.setStyleSheet(f"color: #9ca3af; font-size: 13px; background: transparent; border: none;")
        theme_row.addWidget(theme_lbl)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.setCurrentText(self.current_theme.capitalize())
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        self.theme_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {c['bg_input']};
                color: {c['text_primary']};
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 6px;
                padding: 6px 10px;
                min-height: 22px;
                min-width: 120px;
            }}
        """)
        theme_row.addWidget(self.theme_combo)
        theme_row.addStretch()
        box_layout.addLayout(theme_row)

        # ─ Data Settings
        data_lbl = QLabel("DATA SETTINGS")
        data_lbl.setStyleSheet(f"""
            QLabel {{
                color: {c['accent']};
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1.2px;
                background: transparent;
                border: none;
            }}
        """)
        box_layout.addWidget(data_lbl)

        self.auto_save_check = QCheckBox("Auto-save data on changes")
        self.auto_save_check.setChecked(True)
        self.auto_save_check.setStyleSheet(f"color: {c['text_primary']}; background: transparent; border: none;")
        box_layout.addWidget(self.auto_save_check)

        dec_row = QHBoxLayout()
        dec_lbl = QLabel("Decimal places:")
        dec_lbl.setStyleSheet(f"color: #9ca3af; font-size: 13px; background: transparent; border: none;")
        dec_row.addWidget(dec_lbl)
        self.decimal_spin = QSpinBox()
        self.decimal_spin.setRange(0, 10)
        self.decimal_spin.setValue(2)
        self.decimal_spin.setStyleSheet(f"""
            QSpinBox {{
                background-color: {c['bg_input']};
                color: {c['text_primary']};
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 6px;
                padding: 6px 10px;
                min-height: 22px;
                min-width: 60px;
            }}
        """)
        dec_row.addWidget(self.decimal_spin)
        dec_row.addStretch()
        box_layout.addLayout(dec_row)

        # ─ Visualization
        viz_lbl = QLabel("VISUALIZATION")
        viz_lbl.setStyleSheet(f"""
            QLabel {{
                color: {c['accent']};
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1.2px;
                background: transparent;
                border: none;
            }}
        """)
        box_layout.addWidget(viz_lbl)

        dpi_row = QHBoxLayout()
        dpi_lbl = QLabel("Export DPI:")
        dpi_lbl.setStyleSheet(f"color: #9ca3af; font-size: 13px; background: transparent; border: none;")
        dpi_row.addWidget(dpi_lbl)
        self.dpi_combo = QComboBox()
        self.dpi_combo.addItems(["150", "300", "600"])
        self.dpi_combo.setCurrentText("300")
        self.dpi_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {c['bg_input']};
                color: {c['text_primary']};
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 6px;
                padding: 6px 10px;
                min-height: 22px;
                min-width: 80px;
            }}
        """)
        dpi_row.addWidget(self.dpi_combo)
        dpi_row.addStretch()
        box_layout.addLayout(dpi_row)

        # Close button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        close_btn = QPushButton("Close")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['accent']};
                color: {c['text_inverse']};
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-size: 12px;
                font-weight: 600;
                min-height: 0px;
            }}
            QPushButton:hover {{
                background-color: {c['accent_hover']};
            }}
        """)
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        box_layout.addLayout(btn_layout)

    def _layout_children(self):
        if self.parent():
            self.resize(self.parent().size())
            self.move(self.parent().mapToGlobal(self.parent().rect().topLeft()))
        self._overlay.setGeometry(0, 0, self.width(), self.height())
        box_w = min(480, self.width() - 60)
        self._box.setFixedWidth(box_w)
        self._box.adjustSize()
        bx = (self.width() - box_w) // 2
        by = (self.height() - self._box.height()) // 2
        self._box.move(bx, by)

    def showEvent(self, event):
        super().showEvent(event)
        self._layout_children()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._layout_children()

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
        layout.setContentsMargins(48, 40, 48, 0)
        layout.setSpacing(24)

        # Header
        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setSpacing(6)
        title_label = QLabel("DataLens")
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_layout.addWidget(title_label)

        self.subtitle_label = QLabel("Select a workspace to begin your analysis")
        subtitle_font = QFont()
        subtitle_font.setPointSize(11)
        self.subtitle_label.setFont(subtitle_font)
        title_layout.addWidget(self.subtitle_label)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        self.settings_btn = QPushButton("Settings")
        self.settings_btn.clicked.connect(self.show_settings)
        header_layout.addWidget(self.settings_btn)

        layout.addLayout(header_layout)

        # Separator
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setFixedHeight(1)
        layout.addWidget(self.separator)

        # Workspaces section header
        workspaces_header_layout = QHBoxLayout()

        workspaces_label = QLabel("Your Workspaces")
        workspaces_font = QFont()
        workspaces_font.setPointSize(13)
        workspaces_font.setBold(True)
        workspaces_label.setFont(workspaces_font)
        workspaces_header_layout.addWidget(workspaces_label)

        workspaces_header_layout.addStretch()

        self.create_workspace_btn = QPushButton("+ New Workspace")
        self.create_workspace_btn.setProperty("cssClass", "primary")
        self.create_workspace_btn.clicked.connect(self.create_new_workspace)
        workspaces_header_layout.addWidget(self.create_workspace_btn)

        layout.addLayout(workspaces_header_layout)

        # Scrollable workspace grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.workspaces_container = QWidget()
        self.workspaces_layout = QGridLayout(self.workspaces_container)
        self.workspaces_layout.setSpacing(20)
        self.workspaces_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        scroll_area.setWidget(self.workspaces_container)
        layout.addWidget(scroll_area)

        # ── Footer ──
        c = get_colors(self.current_theme)
        self.footer_frame = QFrame()
        self.footer_frame.setFixedHeight(36)
        footer_layout = QHBoxLayout(self.footer_frame)
        footer_layout.setContentsMargins(48, 0, 48, 0)
        footer_layout.setSpacing(0)

        left_label = QLabel("DataLens")
        left_label.setStyleSheet(f"color: #6b7280; font-size: 11px; background: transparent;")
        footer_layout.addWidget(left_label)

        footer_layout.addStretch()

        center_label = QLabel("\u00a9 2026 DataLens. All rights reserved.")
        center_label.setStyleSheet(f"color: #6b7280; font-size: 11px; background: transparent;")
        center_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout.addWidget(center_label)

        footer_layout.addStretch()

        version_label = QLabel("v1.0.0")
        version_label.setStyleSheet(f"color: #6b7280; font-size: 11px; background: transparent;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        footer_layout.addWidget(version_label)

        layout.addWidget(self.footer_frame)

        self.update_home_theme()

    def update_home_theme(self):
        """Update theme for home screen elements."""
        c = get_colors(self.current_theme)

        self.subtitle_label.setStyleSheet(f"color: {c['text_secondary']}; font-size: 11pt;")
        self.separator.setStyleSheet(f"background-color: {c['border']};")

        self.footer_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {c['bg_secondary']};
                border-top: 1px solid {c['border']};
            }}
        """)

        # Settings uses the global outline style
        self.settings_btn.setProperty("cssClass", "outline")
        self.settings_btn.setStyleSheet("")
        self.settings_btn.style().unpolish(self.settings_btn)
        self.settings_btn.style().polish(self.settings_btn)

        # New workspace uses the global primary style
        self.create_workspace_btn.setProperty("cssClass", "primary")
        self.create_workspace_btn.setStyleSheet("")
        self.create_workspace_btn.style().unpolish(self.create_workspace_btn)
        self.create_workspace_btn.style().polish(self.create_workspace_btn)

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
            c = get_colors(self.current_theme)
            empty_label = QLabel("No workspaces yet. Click '+ New Workspace' to get started!")
            empty_label.setStyleSheet(f"color: {c['text_secondary']}; font-size: 11pt; padding: 40px;")
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

            modal.show_success(
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

                    modal.show_success(
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

            confirmed = modal.show_question(
                self,
                "Delete Workspace",
                f"Are you sure you want to delete '{workspace_name}'?\n\n"
                "This will permanently remove all data, graphs, and reports in this workspace."
            )

            if confirmed:
                import shutil
                try:
                    shutil.rmtree(workspace_path, onerror=self._handle_remove_readonly)
                    self.load_workspaces()

                    modal.show_success(
                        self,
                        "Workspace Deleted",
                        f"Workspace '{workspace_name}' has been deleted."
                    )
                except Exception as e:
                    modal.show_error(
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
