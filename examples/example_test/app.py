import sys
sys.path.append('D:/MyCodes/PyqtProjects/PyQtNodeEditor')
sys.path.append('D:/MyCodes/PyqtProjects/PyQtNodeEditor/node_editor_hu')
from PyQt6.QtWidgets import QApplication
from node_editor_hu.node_editor_window import NodeEditorWindow
from rich.traceback import install

install(show_locals=True) # 设置rich为默认的异常输出处理程序

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = NodeEditorWindow()

    sys.exit(app.exec())