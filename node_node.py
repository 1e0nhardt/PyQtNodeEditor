from node_scene import Scene
from node_graphics_node import QDMGraphicsNode
from node_content_widget import QDMNodeContentWidget

class Node(object):

    def __init__(self, scene: Scene, title='Undefined Node') -> None:
        self.scene = scene
        self.title = title

        self.content = QDMNodeContentWidget()
        self.grNode = QDMGraphicsNode(self)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs = []
        self.outputs = []