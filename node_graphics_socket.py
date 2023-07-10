import typing
from PyQt6 import QtCore
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent
from utils import CONSOLE


class QDMGraphicsSocket(QGraphicsItem):

    def __init__(self, parent=None, socket_type=1):
        super().__init__(parent)

        self.radius = 6
        self.outline_width = 1.0

        self._colors = [
            QColor('#FFFF7700'),
            QColor('#FF522e22'),
            QColor('#FF357700'),
            QColor('#FF127745'),
            QColor('#FF993366'),
        ]
        self._color_background = self._colors[socket_type]
        self._color_outline = QColor("#FF000000")

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)

        self._brush = QBrush(self._color_background)

    def paint(self, painter, option, widget=None) -> None:
        # 画圆点
        painter.setPen(self._pen)
        painter.setBrush(self._brush)
        painter.drawEllipse(-self.radius, -self.radius, 2*self.radius, 2*self.radius)
    
    def boundingRect(self) -> QRectF:
        return QRectF(
            -self.radius-self.outline_width, -self.radius-self.outline_width,
            2*self.radius + self.outline_width, 2*self.radius + self.outline_width
        )
