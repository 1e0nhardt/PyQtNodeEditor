from collections import OrderedDict
import typing
from node_editor_hu.node_graphics_edge import QDMGraphicsEdgeDirect, QDMGraphicsEdgeBezier
from node_editor_hu.utils import logger
from node_editor_hu.node_serializable import Serializable

if typing.TYPE_CHECKING:
    from node_editor_hu.node_socket import Socket
    from node_editor_hu.node_scene import Scene

EDGE_TYPE_DIRCET=1
EDGE_TYPE_BEZIER=2


class Edge(Serializable):

    def __init__(self, scene: 'Scene', start_socket: 'Socket' = None, end_socket: 'Socket' = None, edge_type = EDGE_TYPE_BEZIER) -> None:
        super().__init__()
        self.scene = scene

        # default init
        self._start_socket = None
        self._end_socket = None

        self.start_socket = start_socket
        self.end_socket = end_socket
        self.edge_type = edge_type

        self.scene.addEdge(self)
    
    @property
    def start_socket(self):
        return self._start_socket
    
    @start_socket.setter
    def start_socket(self, value: 'Socket'):
        if self._start_socket is not None:
            self._start_socket.removeEdge(self)

        # assign new socket and connect to edge
        self._start_socket = value
        if value is not None:
            self._start_socket.addEdge(self)

    @property
    def end_socket(self):
        return self._end_socket
    
    @end_socket.setter
    def end_socket(self, value: 'Socket'):
        if self._end_socket is not None:
            self._end_socket.removeEdge(self)
        
        # assign new socket and connect to edge
        self._end_socket = value
        if  value is not None:
            self._end_socket.addEdge(self)
    
    @property
    def edge_type(self):
        return self._edge_type
    @edge_type.setter
    def edge_type(self, value: int):
        if hasattr(self, 'grEdge') and self.grEdge is not None:
            self.scene.grScene.removeItem(self.grEdge)

        self._edge_type = value

        if value == EDGE_TYPE_DIRCET:
            self.grEdge = QDMGraphicsEdgeDirect(self)
        else:
            self.grEdge = QDMGraphicsEdgeBezier(self)

        if self.start_socket is not None:
            self.updatePosition()

        self.scene.grScene.addItem(self.grEdge)

    def updatePosition(self):
        start_point = self.start_socket.getSocketPosition() # socket相对node的位置
        start_point[0] += self.start_socket.node.grNode.pos().x()
        start_point[1] += self.start_socket.node.grNode.pos().y()
        self.grEdge.setStartPoint(*start_point)

        if self.end_socket is not None:
            dest_point = self.end_socket.getSocketPosition() # socket相对node的位置
            dest_point[0] += self.end_socket.node.grNode.pos().x()
            dest_point[1] += self.end_socket.node.grNode.pos().y()
            self.grEdge.setDestPoint(*dest_point)
        else:
            self.grEdge.setDestPoint(*start_point)
        
        self.grEdge.update()
    
    def remove_from_sockets(self):
        self.start_socket = None
        self.end_socekt = None

    def remove(self):
        logger.debug(f'$ Removing edge {self}')
        logger.debug(f'$  remove edge from all socket')
        self.remove_from_sockets()
        logger.debug(f'$  remove grEdge')
        self.scene.grScene.removeItem(self.grEdge)
        self.grEdge = None
        logger.debug(f'$  remove edge from scene')
        self.scene.removeEdge(self)
        logger.debug(f'$  all done!')
        
    def serialize(self):
        return OrderedDict({
            'id': self.id,
            'edge_type': self.edge_type,
            'start': self.start_socket.id,
            'end': self.end_socket.id,
        })
    
    def deserialize(self, data: OrderedDict, hashmap: typing.Optional[dict] = ..., restore_id: bool = True):
        if restore_id:
            self.id = data['id']
        self.start_socket = hashmap[data['start']]
        self.end_socket = hashmap[data['end']]
        self.edge_type = data['edge_type']
        return True
    
    def __str__(self):
        return f'<Edge {hex(id(self))}>'