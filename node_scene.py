from collections import OrderedDict
from node_graphics_scene import QDMGraphicsScene
from node_serializable import Serializable
import json
from utils import logger

class  Scene(Serializable):

    def __init__(self) -> None:
        super().__init__()
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

    def saveToFile(self, filename):
        logger.info(f'saving to {filename}')
        with open(filename, 'w') as file:
            file.write(json.dumps(self.serialize(), indent=4))
    
    def loadFromFile(self, filename):
        with open(filename, 'r') as file:
            raw_data = file.read()
            data = json.loads(raw_data, encoding='utf-8')
            self.deserialize(data)

    def serialize(self):
        nodes = [node.serialize() for node in  self.nodes]
        edges = [edge.serialize() for edge in  self.edges]
        return OrderedDict({
            'id': self.id,
            'scene_width': self.scene_width,
            'scene_height': self.scene_height,
            'nodes': nodes,
            'edges': edges
        })
    
    def deserialize(self, data, hashmap=...):
        return False