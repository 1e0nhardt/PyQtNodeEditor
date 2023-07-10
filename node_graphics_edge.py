import typing
from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QStyleOptionGraphicsItem, QWidget


class QDMGraphicsEdge(QGraphicsPathItem):

    def __init__(self, edge, parent=None):
        super().__init__(parent)
        self.edge = edge

        self.pointStart = [-100, -100]
        self.pointDest = [100, 100]

        self._color_defalut = QColor('#001000')
        self._color_selected = QColor('#00FF00')
        self._pen_defalut = QPen(self._color_defalut)
        self._pen_defalut.setWidthF(1.5)
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(1.5)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.setZValue(-1)

    def paint(self, painter, option, widget=None) -> None:
        self.updatePath()

        painter.setPen(self._pen_defalut if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(self.path())
    
    def updatePath(self):
        raise NotImplemented('This method has to be implemented in a child class')
    

class QDMGraphicsEdgeDirect(QDMGraphicsEdge):

    def updatePath(self):
        path = QPainterPath(QPointF(self.pointStart[0], self.pointStart[1]))
        path.lineTo(self.pointDest[0], self.pointDest[1])
        self.setPath(path)


class QDMGraphicsEdgeBezier(QDMGraphicsEdge):

    def updatePath(self):
        s = self.pointStart
        d = self.pointDest
        
        dist = (d[0] - s[0]) * 0.5
        if dist < 0: dist *= -1
        
        path = QPainterPath(QPointF(s[0], s[1]))
        path.cubicTo(s[0] + dist, s[1], d[0]-dist, d[1], d[0], d[1])
        self.setPath(path)
