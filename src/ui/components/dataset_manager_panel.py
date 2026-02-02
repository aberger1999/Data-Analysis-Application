"""
Dataset manager dialog for managing datasets within a workspace.
"""

import os
import shutil
from datetime import datetime
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox, QFileDialog,
    QInputDialog, QLabel, QMenu, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QFont, QColor

class DatasetItem(QWidget):
    """Custom widget for dataset list items."""

    def __init__(self, filename, file_path, is_active=False):
        super().__init__()
        self.filename = filename
        self.file_path = file_path
        self.is_active = is_active

        # Set fixed height to prevent cutoff
        self.setMinimumHeight(80)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        file_size = os.path.getsize(file_path)
        size_str = self.format_size(file_size)

        mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        time_str = mod_time.strftime("%Y-%m-%d %H:%M")

        name_without_ext = filename.replace('.csv', '')

        info_layout = QVBoxLayout()
        info_layout.setSpacing(6)
        info_layout.setContentsMargins(0, 0, 0, 0)

        name_label = QLabel(name_without_ext)
        name_label.setStyleSheet("font-weight: bold; font-size: 13pt; color: #1e1e1e;")
        name_label.setWordWrap(False)
        name_label.setFixedHeight(22)

        details_label = QLabel(f"{size_str} • {time_str}")
        details_label.setStyleSheet("color: #666; font-size: 10pt;")
        details_label.setFixedHeight(18)

        info_layout.addWidget(name_label)
        info_layout.addWidget(details_label)
        info_layout.addStretch()

        layout.addLayout(info_layout, 1)

        self.menu_btn = QPushButton("⋮")
        self.menu_btn.setFixedSize(36, 36)
        self.menu_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 20pt;
                color: #666;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border-radius: 6px;
                color: #333;
            }
        """)
        layout.addWidget(self.menu_btn, 0, Qt.AlignmentFlag.AlignVCenter)

    def format_size(self, size):
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

class DatasetManagerDialog(QDialog):
    """Dialog for managing datasets in a workspace."""

    dataset_selected = pyqtSignal(str)
    dataset_deleted = pyqtSignal(str)
    dataset_renamed = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.workspace_path = None
        self.current_dataset = "workspace_data.csv"
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Dataset Manager")
        self.setModal(True)
        self.setMinimumSize(750, 550)

        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)

        header = QLabel("📊 Dataset Manager")
        header.setStyleSheet("font-size: 18pt; font-weight: bold; color: #1e1e1e;")
        layout.addWidget(header)

        self.dataset_list = QListWidget()
        self.dataset_list.setSpacing(4)
        self.dataset_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 8px;
                outline: none;
            }
            QListWidget::item {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 0px;
                margin: 4px;
                min-height: 80px;
            }
            QListWidget::item:hover {
                background-color: #f8f8f8;
                border: 1px solid #ccc;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                border: 2px solid #2196F3;
            }
        """)
        self.dataset_list.itemDoubleClicked.connect(self.load_selected_dataset)
        layout.addWidget(self.dataset_list)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.import_btn = QPushButton("📁 Import Dataset")
        self.import_btn.clicked.connect(self.import_dataset)
        self.import_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 14px 28px;
                font-size: 12pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)

        self.load_btn = QPushButton("✓ Load Selected")
        self.load_btn.clicked.connect(self.load_selected_dataset)
        self.load_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 14px 28px;
                font-size: 12pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 14px 28px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)

        button_layout.addWidget(self.import_btn)
        button_layout.addWidget(self.load_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)

        layout.addLayout(button_layout)

    def set_workspace(self, workspace_path):
        """Set the workspace path and refresh the dataset list."""
        self.workspace_path = workspace_path
        self.refresh_dataset_list()

    def set_current_dataset(self, filename):
        """Set the currently active dataset."""
        self.current_dataset = filename
        self.refresh_dataset_list()

    def refresh_dataset_list(self):
        """Refresh the list of datasets."""
        self.dataset_list.clear()

        if not self.workspace_path:
            return

        data_folder = os.path.join(self.workspace_path, "data")
        if not os.path.exists(data_folder):
            return

        csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
        csv_files.sort()

        for filename in csv_files:
            file_path = os.path.join(data_folder, filename)
            is_active = (filename == self.current_dataset)

            item = QListWidgetItem(self.dataset_list)
            widget = DatasetItem(filename, file_path, is_active)

            widget.menu_btn.clicked.connect(lambda checked, f=filename: self.show_context_menu(f))

            item.setSizeHint(widget.sizeHint())
            self.dataset_list.addItem(item)
            self.dataset_list.setItemWidget(item, widget)

            if is_active:
                item.setSelected(True)

    def show_context_menu(self, filename):
        """Show context menu for dataset actions."""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 6px;
            }
            QMenu::item {
                padding: 10px 28px;
                color: #1e1e1e;
                font-size: 11pt;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #2196F3;
                color: white;
            }
        """)

        rename_action = menu.addAction("✏️ Rename")
        delete_action = menu.addAction("🗑️ Delete")

        if filename == "workspace_data.csv":
            rename_action.setEnabled(False)

        action = menu.exec(self.sender().mapToGlobal(self.sender().rect().bottomLeft()))

        if action == rename_action:
            self.rename_dataset(filename)
        elif action == delete_action:
            self.delete_dataset(filename)

    def import_dataset(self):
        """Import a new dataset from a CSV file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Dataset",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )

        if not file_path:
            return

        try:
            filename = os.path.basename(file_path)
            dest_path = os.path.join(self.workspace_path, "data", filename)

            if os.path.exists(dest_path):
                reply = QMessageBox.question(
                    self,
                    "File Exists",
                    f"A dataset named '{filename}' already exists. Overwrite?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.No:
                    return

            shutil.copy2(file_path, dest_path)
            self.refresh_dataset_list()

            QMessageBox.information(
                self,
                "Success",
                f"Dataset '{filename}' imported successfully!"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error importing dataset: {str(e)}"
            )

    def load_selected_dataset(self):
        """Load the selected dataset."""
        current_item = self.dataset_list.currentItem()
        if not current_item:
            return

        widget = self.dataset_list.itemWidget(current_item)
        if not widget:
            return

        file_path = widget.file_path
        self.dataset_selected.emit(file_path)
        self.set_current_dataset(widget.filename)

    def rename_dataset(self, filename):
        """Rename a dataset."""
        if filename == "workspace_data.csv":
            QMessageBox.warning(
                self,
                "Cannot Rename",
                "The active workspace data file cannot be renamed."
            )
            return

        name_without_ext = filename.replace('.csv', '')
        new_name, ok = QInputDialog.getText(
            self,
            "Rename Dataset",
            "Enter new name:",
            text=name_without_ext
        )

        if not ok or not new_name:
            return

        if not new_name.endswith('.csv'):
            new_name += '.csv'

        try:
            old_path = os.path.join(self.workspace_path, "data", filename)
            new_path = os.path.join(self.workspace_path, "data", new_name)

            if os.path.exists(new_path):
                QMessageBox.warning(
                    self,
                    "Error",
                    f"A dataset named '{new_name}' already exists."
                )
                return

            os.rename(old_path, new_path)
            self.dataset_renamed.emit(filename, new_name)
            self.refresh_dataset_list()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error renaming dataset: {str(e)}"
            )

    def delete_dataset(self, filename):
        """Delete a dataset."""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{filename}'?\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.No:
            return

        try:
            file_path = os.path.join(self.workspace_path, "data", filename)
            os.remove(file_path)
            self.dataset_deleted.emit(filename)
            self.refresh_dataset_list()

            QMessageBox.information(
                self,
                "Success",
                f"Dataset '{filename}' deleted successfully!"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error deleting dataset: {str(e)}"
            )
