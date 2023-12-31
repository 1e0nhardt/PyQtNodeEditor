import typing
from node_editor_hu.node_graphics_node import QDMGraphicsNode
from node_editor_hu.node_content_widget import QDMNodeContentWidget
from node_editor_hu.node_socket import *
from node_editor_hu.utils import logger
from node_editor_hu.node_serializable import Serializable
from collections import OrderedDict

if typing.TYPE_CHECKING:
    from node_editor_hu.node_scene import Scene

class Node(Serializable):

    def __init__(self, scene: 'Scene', title: str = 'Undefined Node', inputs: typing.List[int] = [], outputs: typing.List[int] = []) -> None:
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
            socket = Socket(self, index, position=BOTTOM_LEFT, socket_type=item, multi_edges=False)
            self.inputs.append(socket)
        
        for index, item in enumerate(outputs):
            socket = Socket(self, index, position=TOP_RIGHT, socket_type=item, multi_edges=True)
            self.outputs.append(socket)
    
    def getSocketPosition(self, index: int, position: int):
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
    def title(self, value: str):
        self._title = value
        self.grNode.title = value

    def setPos(self, x: float, y: float):
        self.grNode.setPos(x, y)

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            for edge in socket.edges:
                edge.updatePosition()
    
    def remove(self):
        logger.debug(f'$ Removing node {self}')
        logger.debug(f'$  remove all edges')
        for socket in self.inputs + self.outputs:
            for edge in socket.edges:
                logger.debug(f'$    remove edge {edge} from socket {socket}')
                edge.remove()
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
    
    def deserialize(self, data: OrderedDict, hashmap: typing.Optional[dict] = ..., restore_id: bool = True):
        if restore_id:
            self.id = data['id']
        hashmap[data['id']] = self

        self.setPos(data['pos_x'], data['pos_y'])
        self.title = data['title']

        data['inputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)
        data['outputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)

        for socket_data in data['inputs']:
            socket = Socket(self, socket_data['index'], socket_data['position'], socket_data['socket_type'], multi_edges=socket_data['multi_edges'])
            socket.deserialize(socket_data, hashmap, restore_id)
            self.inputs.append(socket)

        for socket_data in data['outputs']:
            socket = Socket(self, socket_data['index'], socket_data['position'], socket_data['socket_type'], multi_edges=socket_data['multi_edges'])
            socket.deserialize(socket_data, hashmap, restore_id)
            self.outputs.append(socket)

        return True
    
    def __str__(self):
        return f'<Node {hex(id(self))}>'
