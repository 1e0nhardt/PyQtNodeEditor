from collections import OrderedDict

from node_edge import Edge
from node_graphics_edge import QDMGraphicsEdge
from node_node import Node
from utils import logger


class SceneClipboard():
    def __init__(self, scene):
        self.scene = scene

    def serializeSelected(self, delete=False):
        logger.debug('[red]--- copy to clipboard ---[/]')

        sel_nodes, sel_edges, sel_sockets = [], [], {}

        # 保存选中的边和节点
        for item in self.scene.grScene.selectedItems():
            if hasattr(item, 'node'):
                sel_nodes.append(item.node.serialize())
                for socket in (item.node.inputs + item.node.outputs):
                    sel_sockets[socket.id] = socket
            elif isinstance(item, QDMGraphicsEdge):
                sel_edges.append(item.edge)
        
        # debug
        logger.debug(f"  NODES\n    {sel_nodes}")
        logger.debug(f"  EDGES\n    {sel_edges}")
        logger.debug(f"  SOCKETS\n   {sel_sockets}")

        # 去掉只有一个端点在选中节点中的边
        edges_to_remove = []
        for edge in sel_edges:
            if edge.start_socket.id in sel_sockets and edge.end_socket.id in sel_sockets:
                # logger.debug(" edge is ok, connected with both sides")
                pass
            else:
                logger.debug(f"edge {edge} is not connected with both sides")
                edges_to_remove.append(edge)

        for edge in edges_to_remove:
            sel_edges.remove(edge)

        # 序列化剩下的边
        edges_final = []
        for edge in sel_edges:
            edges_final.append(edge.serialize())

        logger.debug(f"final edge list: {edges_final}")

        data = OrderedDict([
            ('nodes', sel_nodes),
            ('edges', edges_final),
        ])

        # 剪切操作，删除选中的节点和边
        if delete:
            self.scene.grScene.views()[0].deleteSelectedItems()
            # store our history
            self.scene.history.storeHistory("Cut out elements from scene")

        return data

    def deserializeFromClipboard(self, data):
        logger.debug(f"deserializating from clipboard {data}")

        hashmap = {}

        # 获取鼠标在场景中的位置
        view = self.scene.grScene.views()[0]
        mouse_scene_pos = view.last_scene_mouse_position

        # 考虑选中多个节点时，所有节点的bounding box。用其左上角定位
        minx, miny= 0,0
        for node_data in data['nodes']:
            x, y = node_data['pos_x'], node_data['pos_y']
            if x < minx: minx = x
            if y < miny: miny = y

        # 创建节点
        for node_data in data['nodes']:
            new_node = Node(self.scene)
            new_node.deserialize(node_data, hashmap, restore_id=False)

            # 调整节点位置
            pos = new_node.pos
            offset_x, offset_y = pos.x() - minx, pos.y() - miny # 原节点相对于总bounding box的位移
            new_node.setPos(mouse_scene_pos.x() + offset_x, mouse_scene_pos.y() + offset_y) # 鼠标位置设为定位锚点

        # 连接边
        if 'edges' in data:
            for edge_data in data['edges']:
                new_edge = Edge(self.scene)
                new_edge.deserialize(edge_data, hashmap, restore_id=False)

        # store history
        self.scene.history.storeHistory("Pasted elements in scene")

