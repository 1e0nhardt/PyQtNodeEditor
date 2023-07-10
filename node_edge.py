from node_graphics_edge import QDMGraphicsEdgeDirect, QDMGraphicsEdgeBezier

EDGE_TYPE_DIRCET=1
EDGE_TYPE_BEZIER=2


class Edge(object):

    def __init__(self, scene, start_socket, end_socekt, type=EDGE_TYPE_BEZIER) -> None:
        self.scene = scene
        self.start_socket = start_socket
        self.end_socekt = end_socekt

        self.grEdge = QDMGraphicsEdgeBezier(self) if type==EDGE_TYPE_BEZIER else QDMGraphicsEdgeDirect(self)
        self.scene.grScene.addItem(self.grEdge)