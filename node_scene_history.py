import typing

from node_graphics_edge import QDMGraphicsEdge
from utils import logger

if typing.TYPE_CHECKING:
    from node_scene import Scene

class SceneHistory():

    def __init__(self, scene: 'Scene'):
        self.scene = scene

        self.history_stack = []
        self.history_current_step = -1
        self.history_limit = 32

    def undo(self):
        logger.debug("[pink3]UNDO[/]")

        if self.history_current_step > 0:
            self.history_current_step -= 1
            self.restoreHistory()

    def redo(self):
        logger.debug("[pink3]REDO[/]")

        if self.history_current_step + 1 < len(self.history_stack):
            self.history_current_step += 1
            self.restoreHistory()

    def restoreHistory(self):
        logger.debug(f"[pink3]Restoring history[/] .... current_step: #{self.history_current_step} ({len(self.history_stack)})")
        self.restoreHistoryStamp(self.history_stack[self.history_current_step])

    def storeHistory(self, desc):
        # history_current_step没有指向栈头时去除之后的记录。(undo过)
        if self.history_current_step+1 < len(self.history_stack):
            self.history_stack = self.history_stack[0:self.history_current_step+1]

        # 超出历史记录上限时，删除栈尾的记录。
        if self.history_current_step+1 >= self.history_limit:
            self.history_stack = self.history_stack[1:]
            self.history_current_step -= 1
        
        hs = self.createHistoryStamp(desc)
        self.history_stack.append(hs)
        self.history_current_step += 1

        logger.debug(f"[pink3]Storing history[/] {desc} current_step: #{self.history_current_step} ({len(self.history_stack)})")

    def createHistoryStamp(self, desc):
        selected_obj = {
            'nodes': [],
            'edges': [],
        }

        for item in self.scene.grScene.selectedItems():
            if hasattr(item, 'node'):
                selected_obj['nodes'].append(item.node.id)
            elif isinstance(item, QDMGraphicsEdge):
                selected_obj['edges'].append(item.edge.id)

        history_stamp = {
            'desc': desc,
            'snapshot': self.scene.serialize(),
            'selection': selected_obj,
        }

        return history_stamp


    def restoreHistoryStamp(self, history_stamp):
        logger.debug(f"RHS: {history_stamp['desc']}")

        self.scene.deserialize(history_stamp['snapshot'])

        # restore selection
        for edge_id in history_stamp['selection']['edges']:
            for edge in self.scene.edges:
                if edge.id == edge_id:
                    edge.grEdge.setSelected(True)
                    break

        for node_id in history_stamp['selection']['nodes']:
            for node in self.scene.nodes:
                if node.id == node_id:
                    node.grNode.setSelected(True)
                    break

