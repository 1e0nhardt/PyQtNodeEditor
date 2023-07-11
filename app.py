import sys
from PyQt6.QtWidgets import QApplication
from node_editor_wnd import NodeEditorWnd
from rich.traceback import install

install(show_locals=True) # 设置rich为默认的异常输出处理程序

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = NodeEditorWnd()

    sys.exit(app.exec())