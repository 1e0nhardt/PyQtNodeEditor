from collections import OrderedDict
import typing
from node_edge import Edge
from node_graphics_scene import QDMGraphicsScene
from node_node import Node
from node_serializable import Serializable
from node_scene_history import SceneHistory
from node_scene_clipboard import SceneClipboard
import json
from utils import logger

class Scene(Serializable):

    def __init__(self) -> None:
        super().__init__()
        self.nodes = []
        self.edges = []

        self.scene_width = 64000
        self.scene_height = 64000

        self._has_been_modified = False
        self._has_been_modified_listeners = []

        self.history = SceneHistory(self)
        self.clipboard = SceneClipboard(self)

        self.initUI()
    
    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setScene(self.scene_width, self.scene_height)
    
    @property
    def has_been_modified(self):
        return self._has_been_modified

    @has_been_modified.setter
    def has_been_modified(self, value):
        if not self._has_been_modified and value:
            self._has_been_modified = value

            # call all registered listeners
            for callback in self._has_been_modified_listeners:
                callback()

        self._has_been_modified = value

    def addHasBeenModifiedListener(self, callback):
        self._has_been_modified_listeners.append(callback)
    
    def addNode(self, node: Node):
        self.nodes.append(node)
    
    def addEdge(self, edge: Edge):
        self.edges.append(edge)
    
    def removeNode(self, node: Node):
        self.nodes.remove(node)
    
    def removeEdge(self, edge: Edge):
        if edge in self.edges: # 防止重复删除边时报错
            self.edges.remove(edge)
    
    def clear(self):
        while len(self.nodes) > 0:
            self.nodes[0].remove()
        
        self.has_been_modified = False

    def saveToFile(self, filename: str):
        logger.info(f'saving to {filename}')
        with open(filename, 'w') as file:
            file.write(json.dumps(self.serialize(), indent=4))
        
        logger.info("saving to", filename, "was successfull.")
        self.has_been_modified = False

    def loadFromFile(self, filename: str):
        with open(filename, 'r') as file:
            raw_data = file.read()
            data = json.loads(raw_data)
            self.deserialize(data)
            
        self.has_been_modified = False

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
    
    def deserialize(self, data: OrderedDict, hashmap: typing.Optional[dict] = ..., restore_id: bool = True):
        self.clear()
        hashmap = {}

        if restore_id:
            self.id = data['id']

        for node_data in data['nodes']:
            Node(self).deserialize(node_data, hashmap, restore_id)
        
        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, hashmap, restore_id)

        # logger.debug(hashmap)

        return True