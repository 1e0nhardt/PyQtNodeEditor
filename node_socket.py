from node_graphics_socket import QDMGraphicsSocket

TOP_LEFT = 1
BOTTOM_LEFT = 2
TOP_RIGHT = 3
BOTTOM_RIGHT = 4

class Socket(object):

    def __init__(self, node, index=0, position=TOP_LEFT) -> None:
        self.node = node
        self.index = index
        self.position = position

        self.qrSocket = QDMGraphicsSocket(self.node.grNode)
        self.qrSocket.setPos(*self.node.getSocketPosition(index, position))
