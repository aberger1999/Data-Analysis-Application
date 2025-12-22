# -*- coding: utf-8 -*-
"""
Runtime hook to properly configure PyQt6 paths for PyInstaller bundle.
This runs BEFORE the main application starts.
"""

import os
import sys

def setup_qt_environment():
    """Configure Qt plugin and library paths for the frozen executable."""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundle
        base_path = sys._MEIPASS
        
        # Possible Qt plugin locations
        plugin_paths = [
            os.path.join(base_path, 'PyQt6', 'Qt6', 'plugins'),
            os.path.join(base_path, 'PyQt6', 'Qt', 'plugins'),
            os.path.join(base_path, 'plugins'),
        ]
        
        # Find and set the Qt plugin path
        for plugin_path in plugin_paths:
            if os.path.exists(plugin_path):
                os.environ['QT_PLUGIN_PATH'] = plugin_path
                break
        
        # Add base path to system PATH for DLL loading
        current_path = os.environ.get('PATH', '')
        os.environ['PATH'] = base_path + os.pathsep + current_path
        
        # Add Qt bin directory if it exists
        qt_bin_paths = [
            os.path.join(base_path, 'PyQt6', 'Qt6', 'bin'),
            os.path.join(base_path, 'PyQt6', 'Qt', 'bin'),
        ]
        
        for qt_bin in qt_bin_paths:
            if os.path.exists(qt_bin):
                os.environ['PATH'] = qt_bin + os.pathsep + os.environ['PATH']
                break

# Run setup immediately when hook is loaded
setup_qt_environment()
