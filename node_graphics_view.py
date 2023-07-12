from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from node_edge import Edge
from node_graphics_edge import QDMGraphicsEdge

from node_graphics_socket import QDMGraphicsSocket
from utils import logger

MODE_NOOP = 1
MODE_DRAG_EDGE = 2


class QDMGraphicsView(QGraphicsView):

    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene

        self.initUI()

        self.setScene(self.grScene)

        self.mode = MODE_NOOP
        self.edge_drag_threshold_sq = 10 ** 2

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

    #! event
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
    
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        return
    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.mode == MODE_DRAG_EDGE:
            pos = self.mapToScene(event.pos())
            self.drag_edge.grEdge.setDestPoint(pos.x(), pos.y())
            self.drag_edge.grEdge.update() # 立即重绘
        super().mouseMoveEvent(event)

    #! middle mouse button handlers
    def middleMouseButtonPressHandler(self, event: QMouseEvent):
        # type()：返回事件类型
        # button()：返回鼠标事件所涉及的按钮
        # buttons()：返回当前按下的鼠标按钮的状态
        # modifiers()：返回与鼠标事件同时按下的修饰键
        logger.debug(f'scene pos: {event.scenePosition()}, rel pos: {event.position()}, scene pos: {self.mapToScene(event.scenePosition().toPoint())}')
        releaseEvent = QMouseEvent(QEvent.Type.MouseButtonRelease, event.position(), event.globalPosition(),
                                    Qt.MouseButton.LeftButton, Qt.MouseButton.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.position(), event.globalPosition(),
                                    Qt.MouseButton.LeftButton, event.buttons() | Qt.MouseButton.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)
    
    def middleMouseButtonReleaseHandler(self, event: QMouseEvent):
        fakeEvent = QMouseEvent(event.type(), event.position(), event.globalPosition(),
                                    Qt.MouseButton.LeftButton, event.buttons() | Qt.MouseButton.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

    #! left mouse button handlers
    def leftMouseButtonPressHandler(self, event: QMouseEvent):
        item = self.getItemAtClicked(event)
        self.last_lmb_press_pos = self.mapToScene(event.pos())

        if item is None:
            self.selecting = True
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        
        logger.debug(f'LMB Press on {item}')

        # logic
        # Shift+Select
        if hasattr(item, 'node') or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                event.ignore()
                # 模拟Ctrl+LMB点击事件
                fake_event = QMouseEvent(QEvent.Type.MouseButtonPress, event.position(), event.globalPosition(), 
                            Qt.MouseButton.LeftButton, event.buttons() | Qt.MouseButton.LeftButton,
                            event.modifiers() | Qt.KeyboardModifier.ControlModifier)
                super().mousePressEvent(fake_event)
                return

        # Dragging Edge        
        if type(item) is QDMGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_DRAG_EDGE
                self.edgeDragStart(item)
                return
        
        if self.mode == MODE_DRAG_EDGE:
            retFlag = self.edgeDragEnd(item)
            if retFlag:  return
        
        super().mousePressEvent(event)
            
    def leftMouseButtonReleaseHandler(self, event: QMouseEvent):
        item = self.getItemAtClicked(event)

        self.selecting = False
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

        # logger.debug(f'LMB Release on {item}')

        # logic
        # Shift+Select on 'Node', Edge, background
        if hasattr(item, 'node') or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                event.ignore()
                # 模拟Ctrl+LMB释放事件
                fake_event = QMouseEvent(event.type(), event.position(), event.globalPosition(), 
                            Qt.MouseButton.LeftButton, Qt.MouseButton.NoButton,
                            event.modifiers() | Qt.KeyboardModifier.ControlModifier)
                super().mouseReleaseEvent(fake_event)
                return

        # End Dragging Edge    
        if self.mode == MODE_DRAG_EDGE:
            logger.debug('[dark_orange]View::LMBRelease[/] before edgeDragEnd')
            if self.distBetweenClickAndReleaseIsOff(event):
                logger.debug('[dark_orange]View::LMBRelease[/] dist not off')
                retFlag = self.edgeDragEnd(item)
                if retFlag:  return

        super().mouseReleaseEvent(event)
    
    #! right mouse button handlers
    def rightMouseButtonPressHandler(self, event: QMouseEvent):
        super().mousePressEvent(event)
        item = self.getItemAtClicked(event)
        
        if isinstance(item, QDMGraphicsEdge):
            logger.debug(f'RMB DEBUG: {item.edge} connectting sockets {item.edge.start_socket} <---> {item.edge.end_socket}')
        elif type(item) is QDMGraphicsSocket:
            logger.debug(f'RMB DEBUG: {item.socket} has {item.socket.edge}')
        elif item is None:
            logger.debug(f'SCENE: {self.scene}')
            logger.debug(f'  NODES:')
            for node in self.grScene.scene.nodes:
                logger.debug(f'    {node}')
            logger.debug(f'  EDGES:')
            for edge in self.grScene.scene.edges:
                logger.debug(f'    {edge}')
        else:
            logger.debug(f'RMB DEBUG: {item}')

    def rightMouseButtonReleaseHandler(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
    
    #! logic functions
    def distBetweenClickAndReleaseIsOff(self, event):
        new_lmb_press_pos = self.mapToScene(event.pos())
        mouse_move_dist = new_lmb_press_pos - self.last_lmb_press_pos
        logger.debug(f'Distance: {mouse_move_dist}')
        return mouse_move_dist.x()**2 + mouse_move_dist.y()**2 > self.edge_drag_threshold_sq
    
    def edgeDragStart(self, item):
        logger.debug('[dark_orange]View::edgeDragStart[/] $ Start dragging edge')
        logger.debug('[dark_orange]View::edgeDragStart[/] $   get previouse edge')
        self.previous_edge = item.socket.edge # 起始socket是否已经有边
        self.last_start_socket = item.socket
        logger.debug('[dark_orange]View::edgeDragStart[/] $   assign start socket')
        self.drag_edge = Edge(self.grScene.scene, item.socket, None)
        logger.debug(f'[dark_orange]View::edgeDragStart[/] $   drag edge {self.drag_edge}')

    def edgeDragEnd(self, item):
        """return True if want to skip event propagate"""
        self.mode = MODE_NOOP
        logger.debug('[dark_orange]View::edgeDragEnd[/] $ End dragging edge')

        if type(item) is QDMGraphicsSocket:
            if item.socket != self.last_start_socket: # 在同一个socket上点击并释放时，无事发生
                logger.debug(f'[dark_orange]View::edgeDragEnd[/] $   assign end sockets {item.socket}')
                #TODO 目前一个socket只能连接一个edge
                # 连接边 
                if self.previous_edge is not None: # 令一个起点只有一个边，之前的边会删除
                    logger.debug(f'[dark_orange]View::edgeDragEnd[/] $   remove previous edge {self.previous_edge} {self.previous_edge.start_socket} <---> {self.previous_edge.end_socket}')
                    self.previous_edge.remove()
                    self.previous_edge = None
                
                # 从右向左连边
                if item.socket.hasEdge():
                    item.socket.edge.remove()

                self.drag_edge.end_socket = item.socket
                self.drag_edge.start_socket.setConnectedEdge(self.drag_edge)
                self.drag_edge.end_socket.setConnectedEdge(self.drag_edge)
                self.drag_edge.updatePosition() # 连接后，虚线立即变实线
                logger.debug(f'[dark_orange]View::edgeDragEnd[/] $   connected edge {self.drag_edge} {self.drag_edge.start_socket} <---> {self.drag_edge.end_socket}')
                return True

        # 删除创建的边
        logger.debug(f'[dark_orange]View::edgeDragEnd[/] $   removing edge {self.drag_edge}')
        self.drag_edge.remove()
        self.drag_edge = None
        # 点击一个socket开始拖动后，又打算取消，在该socket上结束。
        # 此时会从dragging edge调用该方法
        # 如果该socket原来已经连接了一个边，则socket会丢失对边的引用，导致拖动该节点时对应边不更新
        # 但是开始drag时引用已经变了，所以需要手动重新连接
        item.socket.setConnectedEdge(self.previous_edge)
        logger.debug('[dark_orange]View::edgeDragEnd[/] $   edge removed')
        
        return False
    
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
    
    def getItemAtClicked(self, event):
        pos = event.pos()
        return self.itemAt(pos)