import typing
from collections import OrderedDict

from node_graphics_socket import QDMGraphicsSocket
from node_serializable import Serializable
from utils import logger

if typing.TYPE_CHECKING:
    from node_edge import Edge
    from node_node import Node

TOP_LEFT = 1
BOTTOM_LEFT = 2
TOP_RIGHT = 3
BOTTOM_RIGHT = 4

class Socket(Serializable):

    def __init__(self, node: 'Node', index: int = 0, position=TOP_LEFT, socket_type=1, multi_edges: bool = True) -> None:
        super().__init__()
        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type
        self.is_multi_edges = multi_edges

        self.qrSocket = QDMGraphicsSocket(self, self.socket_type)
        self.qrSocket.setPos(*self.node.getSocketPosition(index, position))

        self.edges = []
    
    def getSocketPosition(self):
        return self.node.getSocketPosition(self.index, self.position)

    def addEdge(self, edge: 'Edge'):
        self.edges.append(edge)

    def removeEdge(self, edge: 'Edge'):
        if edge in self.edges:
            self.edges.remove(edge)
        else:
            logger.warn(f'[dark_orange]Socket::removeEdge[/] want to remove edge {edge} from self.edges, but it is not in the list')
    
    def removeAllEdges(self):
        while len(self.edges) > 0:
            edge = self.edges.pop()
            edge.remove()
    
    def serialize(self):
        return OrderedDict({
            'id': self.id,
            'index': self.index,
            'position': self.position,
            'socket_type': self.socket_type,
            'multi_edges': self.is_multi_edges
        })
    
    def deserialize(self, data: OrderedDict, hashmap: typing.Optional[dict] = ..., restore_id: bool = True):
        if restore_id:
            self.id = data['id']
        hashmap[data['id']] = self
        return True
    
    def __str__(self):
        return f"<Socket {hex(id(self))} {'ME' if self.is_multi_edges else 'SE'}> has Edge {self.edges}"