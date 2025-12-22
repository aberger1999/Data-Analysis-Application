import sys
import os

# Add src to python path so we can import as if we were in src or root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ui.components.workspace_view import WorkspaceView
    print("Successfully imported WorkspaceView")
except Exception as e:
    print(f"Failed to import: {e}")
    import traceback
    traceback.print_exc()
