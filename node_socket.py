from node_graphics_socket import QDMGraphicsSocket

TOP_LEFT = 1
BOTTOM_LEFT = 2
TOP_RIGHT = 3
BOTTOM_RIGHT = 4

class Socket(object):

    def __init__(self, node, index=0, position=TOP_LEFT, socket_type=1) -> None:
        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type

        self.qrSocket = QDMGraphicsSocket(self.node.grNode, self.socket_type)
        self.qrSocket.setPos(*self.node.getSocketPosition(index, position))

        self.edge = None
    
    def getSocketPosition(self):
        return self.node.getSocketPosition(self.index, self.position)

    def setConnectedEdge(self, edge):
        self.edge = edge

    def hasEdge(self):
        return self.edge is not None