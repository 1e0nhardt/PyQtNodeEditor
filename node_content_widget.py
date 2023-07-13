from collections import OrderedDict
from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from utils import logger
from node_serializable import Serializable


class QDMNodeContentWidget(QWidget, Serializable):
    
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node

        self.initUI()

    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self.widget_label = QLabel('SomeTitle')
        self._layout.addWidget(self.widget_label)
        self._layout.addWidget(QDMTextEdit('foo'))
    
    def setEditingFlag(self, flag):
        self.node.scene.grScene.views()[0].editing_flag = flag
    
    def serialize(self):
        return OrderedDict({
            'id': self.id
        })
    
    def deserialize(self, data, hashmap=...):
        return False
    

class QDMTextEdit(QTextEdit):

    # 先触发View的event，再触发TextEdit的。
    # def keyPressEvent(self, event: QKeyEvent) -> None:
    #     logger.debug('QDMTextEdit Key Press') 
    #     super().keyPressEvent(event)

    def focusInEvent(self, event: QFocusEvent) -> None:
        self.parentWidget().setEditingFlag(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        self.parentWidget().setEditingFlag(False)
        super().focusOutEvent(event)