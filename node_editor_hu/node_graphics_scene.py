import math
import typing

from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

if typing.TYPE_CHECKING:
    from node_editor_hu.node_scene import Scene

class QDMGraphicsScene(QGraphicsScene):
    
    def __init__(self, scene: 'Scene', parent=None):
        super().__init__(parent)
        self.scene = scene

        # settings
        self.grid_size = 20
        self.grid_square = 4

        self._color_background = QColor('#393939')
        self._color_light = QColor('#2f2f2f')
        self._color_dark = QColor('#292929')

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        self.setBackgroundBrush(self._color_background)
    
    def setScene(self, width: float, height: float):
        self.setSceneRect(-width//2, -height//2, width, height)

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        super().drawBackground(painter, rect)
        
        # create grid
        left = int(math.floor(rect.left()))
        right = int(math.floor(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.floor(rect.bottom()))

        # compute all lines
        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_square) == 0:
                lines_dark.append(QLine(x, top, x, bottom))
            else:
                lines_light.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_square) == 0:
                lines_dark.append(QLine(left, y, right, y))
            else:
                lines_light.append(QLine(left, y, right, y))
            

        # draw lines
        painter.setPen(self._pen_light)
        painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        painter.drawLines(*lines_dark)