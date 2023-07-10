import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from node_scene import Scene
from node_graphics_view import QDMGraphicsView
from node_node import Node


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
        self.scene = Scene()
        # self.grScene = self.scene.grScene
        
        node = Node(self.scene, 'My Awesome Node')

        # create graph view
        self.view = QDMGraphicsView(self.scene.grScene)
        self._layout.addWidget(self.view)

        self.setWindowTitle('Node Editor')
        self.show()

        # self.addDebugContent()
    
    def addDebugContent(self):
        green_brush = QBrush(Qt.GlobalColor.green)
        outline_pen = QPen(Qt.GlobalColor.black)
        outline_pen.setWidth(2)

        rect = self.grScene.addRect(-100, -100, 80, 100, outline_pen, green_brush)
        rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable) # 让矩形可以拖动

        text = self.grScene.addText('This is some text content', QFont('consolas'))
        text.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        text.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 0.6))

        widget1 = QPushButton('Click Me')
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        proxy2.setPos(0, 60)

        line = self.grScene.addLine(-100, -200, 100, 0)
        line.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        line.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
