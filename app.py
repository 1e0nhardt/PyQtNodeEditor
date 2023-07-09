import sys
from PyQt6.QtWidgets import *
from node_editor_wnd import NodeEditorWnd

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = NodeEditorWnd()

    sys.exit(app.exec())