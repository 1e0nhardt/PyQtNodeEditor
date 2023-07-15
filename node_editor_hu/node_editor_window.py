import json
import os
import typing

from PyQt6.QtGui import QAction, QCloseEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QMessageBox

from node_editor_hu.node_editor_widget import NodeEditorWidget


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
        edit_menu.addAction(self.createAct('Cu&t', 'Ctrl+X', "Cut to clipboard", self.onEditCut))
        edit_menu.addAction(self.createAct('&Copy', 'Ctrl+C', "Copy to clipboard", self.onEditCopy))
        edit_menu.addAction(self.createAct('&Paste', 'Ctrl+V', "Paste from clipboard", self.onEditPaste))
        edit_menu.addSeparator()

        edit_menu.addAction(self.createAct('&Delete', 'Del', "Delete selected items", self.onEditDelete))

        # create node editor widget
        node_editor = NodeEditorWidget(self)
        node_editor.scene.addHasBeenModifiedListener(self.changeTitle)
        self.setCentralWidget(node_editor)

        # status bar
        self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        node_editor.view.scenePosChanged.connect(self.onScenePosChanged)

        # set window properties
        self.setGeometry(200, 200, 800, 600)
        self.changeTitle()
        self.show()
    
    def createAct(self, name: str, shortcut: str, tooltip: str, callback: typing.Callable):
        act = QAction(name, self)
        act.setShortcut(shortcut)
        act.setToolTip(tooltip)
        act.triggered.connect(callback)
        return act

    def changeTitle(self):
        title = "Node Editor - "

        if self.filename is None:
            title += "New"
        else:
            title += os.path.basename(self.filename)

        if self.isModified():
            title += "*"

        self.setWindowTitle(title)

    def closeEvent(self, event: QCloseEvent):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def isModified(self):
        return self.centralWidget().scene.has_been_modified

    def maybeSave(self):
        if not self.isModified():
            return True

        res = QMessageBox.warning(self, "About to loose your work?",
                "The document has been modified.\n Do you want to save your changes?",
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel
              )

        if res == QMessageBox.StandardButton.Save:
            return self.onFileSave()
        elif res == QMessageBox.StandardButton.Cancel:
            return False

        return True

    def onScenePosChanged(self, x: int, y: int):
        self.status_mouse_pos.setText("Scene Pos: [%d, %d]" % (x, y))

    def onFileNew(self):
        if self.maybeSave():
            self.centralWidget().scene.clear()
            self.filename = None
            self.changeTitle()

    def onFileOpen(self):        
        if self.maybeSave():
            fname, filter = QFileDialog.getOpenFileName(self, 'Open graph from file')
            if fname == '':
                return
            if os.path.isfile(fname):
                self.centralWidget().scene.loadFromFile(fname)
                self.filename = fname
                self.changeTitle()

    def onFileSave(self):
        if self.filename is None: return self.onFileSaveAs()
        self.centralWidget().scene.saveToFile(self.filename)
        self.statusBar().showMessage("Successfully saved %s" % self.filename)
        return True

    def onFileSaveAs(self):
        fname, filter = QFileDialog.getSaveFileName(self, 'Save graph to file')
        if fname == '':
            return False
        self.filename = fname
        self.onFileSave()
        return True

    def onEditUndo(self):
        self.centralWidget().scene.history.undo()

    def onEditRedo(self):
        self.centralWidget().scene.history.redo()

    def onEditDelete(self):
        self.centralWidget().scene.grScene.views()[0].deleteSelectedItems()
    
    def onEditCut(self):
        data = self.centralWidget().scene.clipboard.serializeSelected(delete=True)
        str_data = json.dumps(data, indent=4)
        QApplication.instance().clipboard().setText(str_data)

    def onEditCopy(self):
        data = self.centralWidget().scene.clipboard.serializeSelected(delete=False)
        str_data = json.dumps(data, indent=4)
        QApplication.instance().clipboard().setText(str_data)

    def onEditPaste(self):
        raw_data = QApplication.instance().clipboard().text()
        print(raw_data)

        try:
            data = json.loads(raw_data)
        except ValueError as e:
            print("Pasting of not valid json data!", e)
            return

        # check if the json data are correct
        if 'nodes' not in data:
            print("JSON does not contain any nodes!")
            return

        self.centralWidget().scene.clipboard.deserializeFromClipboard(data)





