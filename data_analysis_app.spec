# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Data Analysis Application.
Simplified configuration that uses src/main.py directly as entry point.
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_all

block_cipher = None

# ============================================================================
# Collect PyQt6 - using collect_all for complete collection
# ============================================================================
pyqt6_datas, pyqt6_binaries, pyqt6_hiddenimports = collect_all('PyQt6')

# Collect matplotlib data files
matplotlib_datas = collect_data_files('matplotlib')

# ============================================================================
# Data files
# ============================================================================
all_datas = [
    ('icon.png', '.'),
    ('templates', 'templates'),
    ('assets', 'assets'),
]
all_datas += pyqt6_datas
all_datas += matplotlib_datas

# ============================================================================
# Hidden imports
# ============================================================================
all_hiddenimports = [
    # PyQt6 core
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtGui', 
    'PyQt6.QtWidgets',
    'PyQt6.sip',
    
    # Data analysis
    'pandas',
    'pandas._libs',
    'pandas._libs.tslibs',
    'pandas._libs.tslibs.base',
    'pandas.plotting._matplotlib',
    
    # Numerical
    'numpy',
    'numpy.core._methods',
    'numpy.lib.format',
    
    # Visualization  
    'matplotlib',
    'matplotlib.backends.backend_qt5agg',
    'matplotlib.backends.backend_qtagg',
    'matplotlib.backends.backend_agg',
    'seaborn',
    
    # Scientific
    'scipy',
    'scipy.special',
    'scipy.sparse',
    'scipy.sparse.csgraph',
    'scipy.ndimage',
    
    # Machine learning
    'sklearn',
    'sklearn.ensemble',
    'sklearn.tree',
    'sklearn.linear_model',
    'sklearn.preprocessing',
    'sklearn.model_selection',
    'sklearn.metrics',
    'sklearn.cluster',
    'sklearn.neighbors',
    'sklearn.svm',
    'sklearn.naive_bayes',
    'sklearn.neural_network',
    'sklearn.utils._typedefs',
    'sklearn.neighbors._partition_nodes',
    
    # Excel support
    'openpyxl',
    'xlrd',
    
    # Templating
    'jinja2',
]
all_hiddenimports += pyqt6_hiddenimports

# ============================================================================
# Analysis - use src/main.py as entry point
# ============================================================================

a = Analysis(
    ['src/main.py'],
    pathex=['.', 'src'],
    binaries=pyqt6_binaries,
    datas=all_datas,
    hiddenimports=all_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['qt_runtime_hook.py'],
    excludes=[
        'pytest',
        'pandas.tests',
        'numpy.tests', 
        'sklearn.tests',
        'scipy.tests',
        'matplotlib.tests',
        'tkinter',
        'test',
        'unittest',
        'IPython',
        'notebook',
        'sphinx',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# ============================================================================
# PYZ archive
# ============================================================================

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ============================================================================
# Executable
# ============================================================================

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DataAnalysisApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Keep console to see errors - change to False for release
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)

# ============================================================================
# Collect all files
# ============================================================================

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DataAnalysisApp',
)
