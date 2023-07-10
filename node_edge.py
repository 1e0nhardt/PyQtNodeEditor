from node_graphics_edge import QDMGraphicsEdgeDirect, QDMGraphicsEdgeBezier

EDGE_TYPE_DIRCET=1
EDGE_TYPE_BEZIER=2


class Edge(object):

    def __init__(self, scene, start_socket, end_socket, edge_type=EDGE_TYPE_BEZIER) -> None:
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.start_socket.setConnectedEdge(self)
        if self.end_socket is not None:
            self.end_socket.setConnectedEdge(self)

        self.grEdge = QDMGraphicsEdgeBezier(self) if edge_type==EDGE_TYPE_BEZIER else QDMGraphicsEdgeDirect(self)
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
    
    def remove_from_sockets(self):
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None
        self.start_socket = None
        self.end_socekt = None

    def remove(self):
        self.remove_from_sockets()
        self.scene.grScene.removeItem(self.grEdge)
        self.grEdge = None
        self.scene.removeEdge(self)