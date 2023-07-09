import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import *
from node_graphics_scene import QDMGraphicsScene


class NodeEditorWnd(QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)

        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        # create graph scene
        self.scene = QDMGraphicsScene()

        # create graph view
        self.view = QGraphicsView(self)
        self.view.setScene(self.scene)
        self._layout.addWidget(self.view)

        self.setWindowTitle('Node Editor')
        self.show()