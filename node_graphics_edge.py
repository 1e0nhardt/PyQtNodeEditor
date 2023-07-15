import math
import typing

from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QStyleOptionGraphicsItem, QWidget

from node_socket import *

if typing.TYPE_CHECKING:
    from node_edge import Edge

EDGE_CP_ROUNDNESS = 50.0

class QDMGraphicsEdge(QGraphicsPathItem):

    def __init__(self, edge: 'Edge', parent=None):
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
        self._pen_dragging = QPen(self._color_defalut)
        self._pen_dragging.setWidthF(1.5)
        self._pen_dragging.setStyle(Qt.PenStyle.DashDotLine)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.setZValue(-1)

    def paint(self, painter, option, widget=None) -> None:
        self.calcPath()

        if self.edge.end_socket is None:
            painter.setPen(self._pen_dragging)
        else:
            painter.setPen(self._pen_defalut if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(self.path())
    
    def calcPath(self) -> QPainterPath:
        raise NotImplementedError('This method has to be implemented in a child class')

    def intersectsWith(self, p1: QPointF, p2: QPointF):
        cut_path = QPainterPath(p1)
        cut_path.lineTo(p2)
        path = self.calcPath()
        return cut_path.intersects(path)
    
    def setStartPoint(self, x: float, y: float):
        self.pointStart = [x, y]
    
    def setDestPoint(self, x: float, y: float):
        self.pointDest = [x, y]
    

class QDMGraphicsEdgeDirect(QDMGraphicsEdge):

    def calcPath(self):
        path = QPainterPath(QPointF(self.pointStart[0], self.pointStart[1]))
        path.lineTo(self.pointDest[0], self.pointDest[1])
        self.setPath(path)
        return path


class QDMGraphicsEdgeBezier(QDMGraphicsEdge):

    def calcPath(self):
        s = self.pointStart
        d = self.pointDest
        
        dist = (d[0] - s[0]) * 0.5
        
        cpx_s = dist
        cpx_d = -dist
        cpy_s = 0
        cpy_d = 0

        sspos = self.edge.start_socket.position

        if (s[0] > d[0] and sspos in (TOP_RIGHT, BOTTOM_RIGHT)) or (s[0] < d[0] and sspos in (TOP_LEFT, BOTTOM_LEFT)):
            cpx_d *= -1
            cpx_s *= -1

            cpy_d = ((s[1]-d[1]) / math.fabs(s[1]-d[1]) if (s[1]-d[1]) != 0 else 1e-5) * EDGE_CP_ROUNDNESS

            cpy_s = ((d[1]-s[1]) / math.fabs(d[1]-s[1]) if (d[1]-s[1]) != 0 else 1e-5)* EDGE_CP_ROUNDNESS          
        
        path = QPainterPath(QPointF(s[0], s[1]))
        path.cubicTo(s[0] + cpx_s, s[1] + cpy_s, d[0]+cpx_d, d[1]+cpy_d, d[0], d[1])
        self.setPath(path)
        return path
