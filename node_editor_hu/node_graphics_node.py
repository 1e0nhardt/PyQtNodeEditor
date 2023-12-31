import typing
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent

if typing.TYPE_CHECKING:
    from node_editor_hu.node_node import Node

class QDMGraphicsNode(QGraphicsItem):
    
    def __init__(self, node: 'Node', parent=None) -> None:
        super().__init__(parent)
        self.node = node
        self.content = self.node.content

        self._title_color = QColor(Qt.GlobalColor.white)
        self._title_font = QFont('consolas')

        self.width = 180
        self.height = 240
        self.radius = 10
        self.title_height = 24
        self.title_padding = 8

        self._pen_default = QPen(QColor('#7F000000'))
        self._pen_selected = QPen(QColor('#FFFFA637'))

        self._brush_title = QBrush(QColor('#FF313131'))
        self._brush_background = QBrush(QColor('#E3212121'))

        self.initTitle()
        self.title = self.node.title

        #TODO init socket

        self.initContent()

        self.initUI()

        self.moved_flag = False
    
    def initUI(self):
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
    
    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self.title_padding, 0)
        self.title_item.setTextWidth(self.width - 2*self.title_padding)
    
    def initContent(self):
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(self.radius, self.title_height + self.radius, 
                                self.width - 2*self.radius, self.height - 2*self.radius - self.title_height)
        self.grContent.setWidget(self.content) # 将 QWidget 包装为 QGraphicsItem
    
    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, 
                self.width + 2*self.radius,
                self.height + 2*self.radius
                ).normalized()
    
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, value: str):
        self._title = value
        self.title_item.setPlainText(self._title)
    
    def paint(self, painter, option, widget=None) -> None:
        # 节点标题
        path_title = QPainterPath()
        path_title.setFillRule(Qt.FillRule.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.radius, self.radius)
        path_title.addRect(0, self.title_height - self.radius, self.radius, self.radius)
        path_title.addRect(self.width - self.radius, self.title_height - self.radius, self.radius, self.radius)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # 节点内容
        path_content = QPainterPath()
        path_content.setFillRule(Qt.FillRule.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.radius, self.radius)
        path_content.addRect(0, self.title_height, self.radius, self.radius)
        path_content.addRect(self.width - self.radius, self.title_height, self.radius, self.radius)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # 节点轮廓
        outline = QPainterPath()
        outline.addRoundedRect(0, 0, self.width, self.height, self.radius, self.radius)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(outline)
    
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseMoveEvent(event)
        
        # update all edges connected with selected node
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()
        
        self.moved_flag = True
    
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(event)

        if self.moved_flag:
            self.moved_flag = False
            self.node.scene.history.storeHistory(f'{self.node} moved', setModified=True)