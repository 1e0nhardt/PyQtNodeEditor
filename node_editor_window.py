import os

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from node_editor_widget import NodeEditorWidget


class NodeEditorWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.filename = None

        self.initUI()
    
    def initUI(self):
        menu_bar = self.menuBar()

        # initialize menu
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(self.createAct('&New', 'Ctrl+N', "Create new graph", self.onFileNew))
        file_menu.addSeparator()
        file_menu.addAction(self.createAct('&Open', 'Ctrl+O', "Open file", self.onFileOpen))
        file_menu.addAction(self.createAct('&Save', 'Ctrl+S', "Save file", self.onFileSave))
        file_menu.addAction(self.createAct('Save &As...', 'Ctrl+Shift+S', "Save file as...", self.onFileSaveAs))
        file_menu.addSeparator()
        file_menu.addAction(self.createAct('E&xit', 'Ctrl+Q', "Exit application", self.close))

        edit_menu = menu_bar.addMenu('&Edit')
        edit_menu.addAction(self.createAct('&Undo', 'Ctrl+Z', "Undo last operation", self.onEditUndo))
        edit_menu.addAction(self.createAct('&Redo', 'Ctrl+R', "Redo last operation", self.onEditRedo))
        edit_menu.addSeparator()
        edit_menu.addAction(self.createAct('&Delete', 'Del', "Delete selected items", self.onEditDelete))

        # create node editor widget
        node_editor = NodeEditorWidget(self)
        self.setCentralWidget(node_editor)

        # status bar
        self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        node_editor.view.scenePosChanged.connect(self.onScenePosChanged)

        # set window properties
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle('Node Editor')
        self.show()
    
    def createAct(self, name, shortcut, tooltip, callback):
        act = QAction(name, self)
        act.setShortcut(shortcut)
        act.setToolTip(tooltip)
        act.triggered.connect(callback)
        return act

    def onScenePosChanged(self, x, y):
        self.status_mouse_pos.setText("Scene Pos: [%d, %d]" % (x, y))

    def onFileNew(self):
        self.centralWidget().scene.clear()

    def onFileOpen(self):
        fname, filter = QFileDialog.getOpenFileName(self, 'Open graph from file')
        if fname == '':
            return
        if os.path.isfile(fname):
            self.centralWidget().scene.loadFromFile(fname)

    def onFileSave(self):
        if self.filename is None: return self.onFileSaveAs()
        self.centralWidget().scene.saveToFile(self.filename)
        self.statusBar().showMessage("Successfully saved %s" % self.filename)

    def onFileSaveAs(self):
        fname, filter = QFileDialog.getSaveFileName(self, 'Save graph to file')
        if fname == '':
            return
        self.filename = fname
        self.onFileSave()

    def onEditUndo(self):
        self.centralWidget().scene.history.undo()

    def onEditRedo(self):
        self.centralWidget().scene.history.redo()

    def onEditDelete(self):
        self.centralWidget().scene.grScene.views()[0].deleteSelectedItems()




