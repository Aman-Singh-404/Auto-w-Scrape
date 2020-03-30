import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from Structure_DialogBox import DialogBox
from Structure_Frame import Frame
from Structure_Tree import Tree
from Structure_UrlFeed import UrlFeed
from UI_AutomScra import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.treeF = Frame(self)
        self.treeF.setFixedSize(579, 555)
        self.treeSA.setWidget(self.treeF)

        self.save_flag = True
        self.connect_flag = True
        self.saveto = None

        self.intialheight = self.size().height()
        self.intialwidth = self.size().width()
        self.dialogbox = DialogBox(self)
        self.tree = Tree([self.treeF, self.treeF.size().width(),
                          self.treeF.size().height(), self.dialogbox])

        self.actionNew.triggered.connect(self.newFile)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionExit.triggered.connect(self.close)
        self.actionUrls.triggered.connect(self.importUrls)
        self.actionsaveExcel.triggered.connect(self.savetoExcel)
        # self.actionsaveDB.triggered.connect(self.savetoDB)

        self.addUrlPB.clicked.connect(self.addUrl)
        self.removeUrlPB.clicked.connect(self.removeUrl)
        self.action_nodePB.clicked.connect(self.actionNode)
        self.input_nodePB.clicked.connect(self.inputNode)
        self.data_nodePB.clicked.connect(self.dataNode)
        self.connectorPB.clicked.connect(self.connectNode)

    def actionNode(self):
        levels = 0
        if self.tree.getLevelItems(self.tree.maxLevel) == []:
            levels = self.tree.maxLevel + 1
        else:
            levels = self.tree.maxLevel + 2
        attribute = self.dialogbox.getAction(levels)
        if attribute != None:
            self.tree.createNode("Action", attribute)

    def addUrl(self, url=""):
        index = self.urlsTW.rowCount() + 1
        self.urlsTW.setRowCount(index)
        self.urlsTW.setItem(index - 1, 0, QtWidgets.QTableWidgetItem(url))

    def connectNode(self):
        if self.connect_flag:
            self.tree.enableLabel(False)
            self.connect_flag = False
        else:
            self.tree.enableLabel(True)
            self.connect_flag = True
            self.treeF.connecterdown()

    def dataNode(self):
        levels = 0
        if self.tree.getLevelItems(self.tree.maxLevel) == []:
            levels = self.tree.maxLevel + 1
        else:
            levels = self.tree.maxLevel + 2
        attribute = self.dialogbox.getData(levels)
        if attribute != None:
            self.tree.createNode("Data", attribute)

    def importUrls(self):
        urlfeed = UrlFeed(self)
        for url in urlfeed.run():
            self.addUrl(url)

    def inputNode(self):
        levels = 0
        if self.tree.getLevelItems(self.tree.maxLevel) == []:
            levels = self.tree.maxLevel + 1
        else:
            levels = self.tree.maxLevel + 2
        attribute = self.dialogbox.getInput(levels)
        if attribute != None:
            self.tree.createNode("Input", attribute)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Control and self.connect_flag:
            self.tree.ctrl_flag = False
            self.treeF.ctrl_flag = False
        elif event.key() == QtCore.Qt.Key_Delete and self.connect_flag:
            self.tree.removeNode()
            self.treeF.delete()

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Control:
            self.tree.ctrl_flag = True
            self.treeF.ctrl_flag = True
            self.tree.ctrlOff(False)
    
    def newFile(self):
        pass

    def openFile(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select file", "", "text(*.txt)", options=options)
        print(files)

    def removeUrl(self):
        indices = [i.row()
                   for i in self.urlsTW.selectionModel().selectedRows()]
        indices.reverse()
        for i in indices:
            self.urlsTW.removeRow(i)

    def resizeEvent(self, event):
        incrementwidth = self.size().width() - self.intialwidth
        incrementheight = self.size().height() - self.intialheight
        self.intialwidth = self.size().width()
        self.intialheight = self.size().height()

        self.addUrlPB.move(self.addUrlPB.pos().x(),
                           self.addUrlPB.pos().y() + incrementheight)
        self.removeUrlPB.move(self.removeUrlPB.pos().x(),
                              self.removeUrlPB.pos().y() + incrementheight)
        self.executePB.move(self.executePB.pos().x(),
                            self.executePB.pos().y() + incrementheight)

        self.urlsTW.resize(self.urlsTW.size().width(),
                           self.urlsTW.size().height() + incrementheight)
        self.treeSA.resize(self.treeSA.size().width(
        ) + incrementwidth, self.treeSA.size().height() + incrementheight)

        if (self.treeSA.size().width() - self.treeF.size().width()) * incrementwidth > 0:
            self.tree.width = self.treeSA.size().width()
        if (self.treeSA.size().height() - self.treeF.size().height()) * incrementheight > 0:
            self.tree.height = self.treeSA.size().height()

        for i in range(self.tree.maxLevel + 1):
            self.tree.adjustTreePosition(i, False)

    def saveFile(self):
        name = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", "untitled.txt")
        print(name)

    def savetoExcel(self):
        name = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Data", "untitled.xlsx", "Excel(*.xlsx)")
        self.saveto = [0, name]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
