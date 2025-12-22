import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.components.analysis_panel import AnalysisPanel

# Mock data manager
class MockDataManager:
    def __init__(self):
        # Allow connect to accept arguments
        self.data_loaded = type('Signal', (), {'connect': lambda x=None, y=None: None})()
        self.data = None

try:
    app = QApplication(sys.argv)
    panel = AnalysisPanel(MockDataManager())
    print("AnalysisPanel instantiated successfully")
    
    panel.update_theme("light")
    print("update_theme('light') called successfully")
    
    panel.update_theme("dark")
    print("update_theme('dark') called successfully")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
