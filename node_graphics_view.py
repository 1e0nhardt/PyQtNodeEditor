from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class QDMGraphicsView(QGraphicsView):

    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene

        self.initUI()

        self.setScene(self.grScene)

        self.zoomIn_factor = 1.25
        self.zoom_clamp = True
        self.zoom = 10
        self.zoom_step = 1
        self.zoom_range = [0, 10]
    
    def initUI(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        # 不加这一句，拖动组件时会有残影且部分背景线不能及时重绘
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate) 

        # 去掉滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # 将锚点设为鼠标位置，缩放时鼠标在画布上的位置不变
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    ###########################################################################
    ############################ 鼠标点击事件 ##################################
    ###########################################################################

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonPressHandler(event) # 按下中键移动画布
        elif event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonPressHandler(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonPressHandler(event)
        else:
            super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonReleaseHandler(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonReleaseHandler(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonReleaseHandler(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPressHandler(self, event: QMouseEvent):
        # type()：返回事件类型
        # button()：返回鼠标事件所涉及的按钮
        # buttons()：返回当前按下的鼠标按钮的状态
        # modifiers()：返回与鼠标事件同时按下的修饰键
        releaseEvent = QMouseEvent(QEvent.Type.MouseButtonRelease, event.position(), event.scenePosition(),
                                    Qt.MouseButton.LeftButton, Qt.MouseButton.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.position(), event.scenePosition(),
                                    Qt.MouseButton.LeftButton, event.buttons() | Qt.MouseButton.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)
    
    def middleMouseButtonReleaseHandler(self, event: QMouseEvent):
        fakeEvent = QMouseEvent(event.type(), event.position(), event.scenePosition(),
                                    Qt.MouseButton.LeftButton, event.buttons() | Qt.MouseButton.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

    def leftMouseButtonPressHandler(self, event: QMouseEvent):
        return super().mousePressEvent(event)

    def rightMouseButtonPressHandler(self, event: QMouseEvent):
        return super().mousePressEvent(event)

    def leftMouseButtonReleaseHandler(self, event: QMouseEvent):
        return super().mouseReleaseEvent(event)

    def rightMouseButtonReleaseHandler(self, event: QMouseEvent):
        return super().mouseReleaseEvent(event)
    
    ###########################################################################
    ############################## 滚轮事件 ####################################
    ###########################################################################

    def wheelEvent(self, event: QWheelEvent) -> None:
        zoomOut_factor = 1 / self.zoomIn_factor

        if event.angleDelta().y() > 0:
            zoom_factor = self.zoomIn_factor
            self.zoom += self.zoom_step
        else:
            zoom_factor = zoomOut_factor
            self.zoom -= self.zoom_step
        
        clamp = False
        if self.zoom < self.zoom_range[0]:
            self.zoom, clamp = self.zoom_range[0], True
        elif self.zoom > self.zoom_range[1]:
            self.zoom, clamp = self.zoom_range[1], True
        
        # 画布缩放
        if not clamp or not self.zoom_clamp:
            self.scale(zoom_factor, zoom_factor)