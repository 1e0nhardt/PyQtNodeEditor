from collections import OrderedDict
from node_graphics_socket import QDMGraphicsSocket
from node_serializable import Serializable

TOP_LEFT = 1
BOTTOM_LEFT = 2
TOP_RIGHT = 3
BOTTOM_RIGHT = 4

class Socket(Serializable):

    def __init__(self, node, index=0, position=TOP_LEFT, socket_type=1) -> None:
        super().__init__()
        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type

        self.qrSocket = QDMGraphicsSocket(self, self.socket_type)
        self.qrSocket.setPos(*self.node.getSocketPosition(index, position))

        self.edge = None
    
    def getSocketPosition(self):
        return self.node.getSocketPosition(self.index, self.position)

    def setConnectedEdge(self, edge):
        self.edge = edge

    def hasEdge(self):
        return self.edge is not None
    
    def serialize(self):
        return OrderedDict({
            'id': self.id,
            'index': self.index,
            'position': self.position,
            'socket_type': self.socket_type
        })
    
    def deserialize(self, data, hashmap=..., restore_id=True):
        if restore_id:
            self.id = data['id']
        hashmap[data['id']] = self
        return True
    
    def __str__(self):
        return f'<Socket {hex(id(self))}>'