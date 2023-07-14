import typing

from PyQt6 import QtCore
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from node_graphics_view import QDMGraphicsView
from node_node import Node
from node_scene import Scene
from node_edge import *

from utils import logger


class NodeEditorWidget(QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.stylesheet_filename = 'qss/nodestyle.qss'
        self.loadStyleSheet(self.stylesheet_filename)

        self.initUI()

    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        # create graph scene
        self.scene = Scene()
        # self.grScene = self.scene.grScene
        
        self.addNodes()
        # self.addDebugContent()

        # create graph view
        self.view = QDMGraphicsView(self.scene.grScene)
        self._layout.addWidget(self.view)

    def addNodes(self):
        node1 = Node(self.scene, 'My Awesome Node 1', inputs=[1,2,3], outputs=[1])
        node2 = Node(self.scene, 'My Awesome Node 2', inputs=[1,2,3], outputs=[1])
        node3 = Node(self.scene, 'My Awesome Node 3', inputs=[1,2,3], outputs=[1])
        node1.setPos(-250, -250)
        node2.setPos(150, 20)
        node3.setPos(-150, 50)

        edge1 = Edge(self.scene, node1.outputs[0], node3.inputs[0], edge_type=EDGE_TYPE_DIRCET)
        edge2 = Edge(self.scene, node3.outputs[0], node2.inputs[1], edge_type=EDGE_TYPE_BEZIER)

    def loadStyleSheet(self, filename):
        logger.info(f'[blue]Loading StyleSheet: {filename}[/]')
        file = QFile(filename)
        file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
        styleSheet = file.readAll()
        QApplication.instance().setStyleSheet(str(styleSheet, encoding='utf-8'))
    
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
