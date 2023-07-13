from collections import OrderedDict
from node_graphics_edge import QDMGraphicsEdgeDirect, QDMGraphicsEdgeBezier
from utils import logger
from node_serializable import Serializable

EDGE_TYPE_DIRCET=1
EDGE_TYPE_BEZIER=2


class Edge(Serializable):

    def __init__(self, scene, start_socket, end_socket, edge_type=EDGE_TYPE_BEZIER) -> None:
        super().__init__()
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket
        self.edge_type = edge_type

        self.start_socket.setConnectedEdge(self)
        if self.end_socket is not None:
            self.end_socket.setConnectedEdge(self)

        self.grEdge = QDMGraphicsEdgeBezier(self) if edge_type==EDGE_TYPE_BEZIER else QDMGraphicsEdgeDirect(self)
        self.updatePosition()
        self.scene.grScene.addItem(self.grEdge)
        self.scene.addEdge(self)

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
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None
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
    
    def deserialize(self, data, hashmap=...):
        return super().deserialize(data, hashmap)
    
    def __str__(self):
        return f'<Edge {hex(id(self))}>'