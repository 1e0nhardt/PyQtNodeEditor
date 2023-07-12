from node_graphics_scene import QDMGraphicsScene

class  Scene(object):

    def __init__(self) -> None:
        self.nodes = []
        self.edges = []

        self.scene_width = 64000
        self.scene_height = 64000

        self.initUI()
    
    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setScene(self.scene_width, self.scene_height)
    
    def addNode(self, node):
        self.nodes.append(node)
    
    def addEdge(self, edge):
        self.edges.append(edge)
    
    def removeNode(self, node):
        self.nodes.remove(node)
    
    def removeEdge(self, edge):
        if edge in self.edges: # 防止重复删除边时报错
            self.edges.remove(edge)