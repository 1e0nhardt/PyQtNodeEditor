from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class QDMNodeContentWidget(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self.widget_label = QLabel('SomeTitle')
        self._layout.addWidget(self.widget_label)
        self._layout.addWidget(QTextEdit('foo'))