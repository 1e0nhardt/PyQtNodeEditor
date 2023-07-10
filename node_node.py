from node_scene import Scene
from node_graphics_node import QDMGraphicsNode
from node_content_widget import QDMNodeContentWidget
from node_socket import *

class Node(object):

    def __init__(self, scene: Scene, title='Undefined Node', inputs=[], outputs=[]) -> None:
        self.scene = scene
        self.title = title

        self.content = QDMNodeContentWidget()
        self.grNode = QDMGraphicsNode(self)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.socket_spacing = 22

        self.inputs = []
        self.outputs = []

        for index, item in enumerate(inputs):
            socket = Socket(self, index, position=BOTTOM_LEFT, socket_type=item)
            self.inputs.append(socket)
        
        for index, item in enumerate(outputs):
            socket = Socket(self, index, position=TOP_RIGHT, socket_type=item)
            self.outputs.append(socket)
    
    def getSocketPosition(self, index, position):
        x = 0 if (position in (BOTTOM_LEFT, TOP_LEFT)) else self.grNode.width
        
        if position in (BOTTOM_RIGHT, BOTTOM_LEFT):
            y = self.grNode.height - self.grNode.radius - self.grNode.title_padding - index * self.socket_spacing
        else:
            y = self.grNode.title_height + self.grNode.radius + self.grNode.title_padding + index * self.socket_spacing

        return [x, y]
    
    @property
    def pos(self):
        return self.grNode.pos()

    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePosition()
        