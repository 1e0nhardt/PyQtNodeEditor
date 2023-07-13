from node_graphics_node import QDMGraphicsNode
from node_content_widget import QDMNodeContentWidget
from node_socket import *
from utils import logger
from node_serializable import Serializable
from collections import OrderedDict

class Node(Serializable):

    def __init__(self, scene, title='Undefined Node', inputs=[], outputs=[]) -> None:
        super().__init__()
        self.scene = scene
        self._title = title

        self.content = QDMNodeContentWidget(self)
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
    
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, value):
        self._title = value
        self.grNode.title = value

    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePosition()
    
    def remove(self):
        logger.debug(f'$ Removing node {self}')
        logger.debug(f'$  remove all edges')
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                logger.debug(f'$    remove edge {socket.edge}')
                socket.edge.remove()
        logger.debug(f'$  remove grNode')
        self.scene.grScene.removeItem(self.grNode)
        self.grNode = None
        logger.debug(f'$  remove node from scene')
        self.scene.removeNode(self)
        logger.debug(f'$  all done!')
    
    def serialize(self):
        inputs = [socket.serialize() for socket in  self.inputs]
        outputs = [socket.serialize() for socket in  self.outputs]
        return OrderedDict({
            'id': self.id,
            'title': self.title,
            'pos_x': self.grNode.scenePos().x(),
            'pos_y': self.grNode.scenePos().y(),
            'inputs': inputs,
            'outputs': outputs,
            'content': self.content.serialize()
        })
    
    def deserialize(self, data, hashmap=...):
        self.id = data['id']
        hashmap[data['id']] = self

        self.setPos(data['pos_x'], data['pos_y'])
        self.title = data['title']

        data['inputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)
        data['outputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)

        for socket_data in data['inputs']:
            socket = Socket(self, socket_data['index'], socket_data['position'], socket_data['socket_type'])
            socket.deserialize(socket_data, hashmap)
            self.inputs.append(socket)

        for socket_data in data['outputs']:
            socket = Socket(self, socket_data['index'], socket_data['position'], socket_data['socket_type'])
            socket.deserialize(socket_data, hashmap)
            self.outputs.append(socket)

        return True
    
    def __str__(self):
        return f'<Node {hex(id(self))}>'
