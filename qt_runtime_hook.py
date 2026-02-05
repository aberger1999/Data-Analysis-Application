# -*- coding: utf-8 -*-
"""
Runtime hook to properly configure PyQt5 paths for PyInstaller bundle.
This runs BEFORE the main application starts.
"""

import os
import sys

def setup_qt_environment():
    """Configure Qt plugin and library paths for the frozen executable."""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS

        current_path = os.environ.get('PATH', '')
        os.environ['PATH'] = base_path + os.pathsep + current_path

        internal_path = os.path.join(os.path.dirname(sys.executable), '_internal')
        if os.path.exists(internal_path):
            os.environ['PATH'] = internal_path + os.pathsep + os.environ['PATH']

        plugin_paths = [
            os.path.join(base_path, 'PyQt5', 'Qt5', 'plugins'),
            os.path.join(base_path, 'PyQt5', 'Qt', 'plugins'),
            os.path.join(base_path, 'plugins'),
            os.path.join(internal_path, 'PyQt5', 'Qt5', 'plugins') if os.path.exists(internal_path) else None,
        ]

        for plugin_path in plugin_paths:
            if plugin_path and os.path.exists(plugin_path):
                os.environ['QT_PLUGIN_PATH'] = plugin_path
                break

        qt_bin_paths = [
            os.path.join(base_path, 'PyQt5', 'Qt5', 'bin'),
            os.path.join(base_path, 'PyQt5', 'Qt', 'bin'),
            os.path.join(internal_path, 'PyQt5', 'Qt5', 'bin') if os.path.exists(internal_path) else None,
        ]

        for qt_bin in qt_bin_paths:
            if qt_bin and os.path.exists(qt_bin):
                os.environ['PATH'] = qt_bin + os.pathsep + os.environ['PATH']
                break

        platform_plugin_paths = [
            os.path.join(base_path, 'PyQt5', 'Qt5', 'plugins', 'platforms'),
            os.path.join(base_path, 'PyQt5', 'Qt', 'plugins', 'platforms'),
            os.path.join(base_path, 'plugins', 'platforms'),
            os.path.join(internal_path, 'PyQt5', 'Qt5', 'plugins', 'platforms') if os.path.exists(internal_path) else None,
        ]

        for platform_path in platform_plugin_paths:
            if platform_path and os.path.exists(platform_path):
                os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = platform_path
                break

setup_qt_environment()
