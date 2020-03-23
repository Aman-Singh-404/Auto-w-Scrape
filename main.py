import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from Dialogs import DialogBox
from Label_structure import Label
from Tree_structure import Tree
from UI_AutomScra import Ui_MainWindow


class Connector(QtCore.QRect):
    def __init__(self, inherit, pos):
        self.text = ""
        self.line = None
        self.connectedEnds = []
        self.selected = True

        QtCore.QRect.__init__(self)
        if inherit == "parent":
            self.text = "P"
            self.line = QtCore.QLine(pos.x() + 20, pos.y() - 10, pos.x() + 20, pos.y())
            self.setRect(pos.x() + 10, pos.y() - 30, 20, 20)
        else:
            self.text = "C"
            self.line = QtCore.QLine(pos.x() + 20, pos.y() + 40, pos.x() + 20, pos.y() + 50)
            self.setRect(pos.x() + 10, pos.y() + 50, 20, 20)
    
    def drawConnector(self, painter):
        painter.setPen(QtCore.Qt.black)
        font = QtGui.QFont()
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawLine(self.line)
        if self.selected:
            painter.setBrush(QtCore.Qt.black)
            painter.drawEllipse(self)
            painter.setPen(QtCore.Qt.white)
            painter.drawText(self, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter, self.text)
        else:
            painter.setBrush(QtCore.Qt.white)
            painter.drawEllipse(self)
            painter.setPen(QtCore.Qt.black)
            painter.drawText(self, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter, self.text)
    
    def updateConnector(self, pos):
        if self.text == "P":
            self.line = QtCore.QLine(pos.x() + 20, pos.y() - 10, pos.x() + 20, pos.y())
            self.setRect(pos.x() + 10, pos.y() - 30, 20, 20)
        else:
            self.line = QtCore.QLine(pos.x() + 20, pos.y() + 40, pos.x() + 20, pos.y() + 50)
            self.setRect(pos.x() + 10, pos.y() + 50, 20, 20)    

class Frame(QtWidgets.QFrame):
    def __init__(self, mwindow):
        self.mwindow = mwindow
        self.ctrl_flag = True
        self.type = 0
        self.label = ""
        self.lbl_pos = None
        self.lines = {}
        self.move_line = QtCore.QLine()

        QtWidgets.QFrame.__init__(self)
        self.setObjectName("treeF")
        self.setMouseTracking(True)
        '''
        self.menu = QtWidgets.QMenu(self)

        changeA = QtWidgets.QAction('Change property', self)
        changeA.triggered.connect(self.mouseDoubleClickEvent)
        self.menu.addAction(changeA)

        deleteA = QtWidgets.QAction('Delete node', self)
        deleteA.setShortcut("Del")
        deleteA.triggered.connect(self.tree.removeNode)
        self.menu.addAction(deleteA)
        '''
        self.show()
    
    def connecterdown(self):
        if self.type == 1:
            self.lines[self.label][1] = None
            self.type = 0
            self.update()
    
    def deleteConnector(self, label, faulter):
        for item in faulter[0]:
            self.lines[label][0].connectedEnds.remove(item)
            self.lines[item][1].connectedEnds.remove(label)
            self.mwindow.tree.removeRelations(item, label)
            if self.lines[item][1].connectedEnds == []:
                self.lines[item][1] = None
        if faulter[0] != [] and self.lines[label][0].connectedEnds == []:
            self.lines[label][0] = None
        for item in faulter[1]:
            self.lines[label][1].connectedEnds.remove(item)
            self.lines[item][0].connectedEnds.remove(label)
            self.mwindow.tree.removeRelations(label, item)
            if self.lines[item][0].connectedEnds == []:
                self.lines[item][0] = None
        if faulter[1] != [] and self.lines[label][1].connectedEnds == []:
            self.lines[label][1] = None
    
    def indicateLabel(self, label, pos):
        self.type = (self.type + 1) % 3
        if self.type == 1:
            if self.lines[label][1] == None:
                self.lines[label][1] = Connector("child", pos)
            self.label = label
            self.lbl_pos = QtCore.QPoint(pos.x() + 20, pos.y() + 40)
        elif self.lbl_pos.y() < pos.y():
            if self.lines[label][0] == None:
                self.lines[label][0] = Connector("parent", pos)
            if label not in self.lines[self.label][1].connectedEnds:
                self.lines[self.label][1].connectedEnds.append(label)
                self.lines[label][0].connectedEnds.append(self.label)
                self.mwindow.tree.setRelations(self.label, label)
            self.update()
            self.type = (self.type + 1) % 3
            self.label = ""
            self.mwindow.connect_flag = True
        else:
            self.type = (self.type - 1) % 3
            QtWidgets.QMessageBox.warning(self, 'Alert', "Same or top level connectors are restricted.")
    
    def mouseMoveEvent(self, event):
        if self.type == 1:
            self.move_line = QtCore.QLine(self.lbl_pos, event.pos())
            self.update()
    
    def mousePressEvent(self, event):
        if self.ctrl_flag:
            self.mwindow.tree.clearSelection()
            self.connectorSelection(pos = event.pos())
    
    def mouseDoubleClickEvent(self, event):
        if self.ctrl_flag:
            self.mwindow.tree.clearSelection()
            self.connectorSelection(pos = event.pos())
            frame = QtWidgets.QFrame(self)
            layout = QtWidgets.QHBoxLayout(frame)
            scrollArea = QtWidgets.QScrollArea(frame)
            layout.addWidget(scrollArea)
            layout.addItem("A1")
    
    def connectorSelection(self, pos, label = False):
        for _, conn in self.lines.items():
            if conn[0] != None:
                if conn[0].contains(pos):
                    conn[0].selected = False
                    for item in conn[0].connectedEnds:
                        self.lines[item][1].selected = False
                    break
                elif not conn[0].contains(pos) or label:
                    conn[0].selected = True
            elif conn[1] != None:
                if conn[1].contains(pos):
                    conn[1].selected = False
                    for item in conn[1].connectedEnds:
                        self.lines[item][0].selected = False
                    break
                elif not conn[1].contains(pos) or label:
                    conn[1].selected = True
        self.update()
    
    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        if self.type == 1:
            painter.drawLine(self.move_line)
        for _, conn in self.lines.items():
            if conn[0] != None:
                conn[0].drawConnector(painter)
            if conn[1] != None:
                conn[1].drawConnector(painter)
        painter.end()
    
    def updateconnector(self, update_list):
        for item in update_list:
            position = self.findChild(Label, item).pos()
            if self.lines[item][0] != None:
                self.lines[item][0].updateConnector(position)
            if self.lines[item][1] != None:
                self.lines[item][1].updateConnector(position)
        self.update()

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.treeF = Frame(self)
        self.treeF.setFixedSize(579, 555)
        self.treeSA.setWidget(self.treeF)

        self.lines = {}
        self.connect_flag = True

        self.intialheight = self.size().height()
        self.intialwidth = self.size().width()
        self.dialogbox = DialogBox(self)
        self.tree = Tree([self.treeF, self.treeF.size().width(), self.treeF.size().height(), self.dialogbox])

        self.actionNew.triggered.connect(self.newFile)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionExit.triggered.connect(self.close)

        self.addUrlPB.clicked.connect(self.addUrl)
        self.removeUrlPB.clicked.connect(self.removeUrl)
        self.action_nodePB.clicked.connect(self.actionNode)
        self.input_nodePB.clicked.connect(self.inputNode)
        self.data_nodePB.clicked.connect(self.dataNode)
        self.connectorPB.clicked.connect(self.connectNode)

        for i in range(2):
            self.tree.createNode("Action", [i, "Click", ""])

    def resizeEvent(self, event):
        incrementwidth = self.size().width() - self.intialwidth
        incrementheight = self.size().height() - self.intialheight
        self.intialwidth = self.size().width()
        self.intialheight = self.size().height()
        
        self.addUrlPB.move(self.addUrlPB.pos().x(), self.addUrlPB.pos().y() + incrementheight)
        self.removeUrlPB.move(self.removeUrlPB.pos().x(), self.removeUrlPB.pos().y() + incrementheight)
        self.executePB.move(self.executePB.pos().x(), self.executePB.pos().y() + incrementheight)
        
        self.urlsTW.resize(self.urlsTW.size().width(), self.urlsTW.size().height() + incrementheight)
        self.treeSA.resize(self.treeSA.size().width() + incrementwidth, self.treeSA.size().height() + incrementheight)

        if (self.treeSA.size().width() - self.treeF.size().width()) * incrementwidth > 0:
            self.tree.width = self.treeSA.size().width()
        if (self.treeSA.size().height() - self.treeF.size().height()) * incrementheight > 0:
            self.tree.height = self.treeSA.size().height()

        for i in range(self.tree.maxLevel + 1):
            self.tree.adjustTreePosition(i, False)

    def newFile(self):
        pass

    def openFile(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select file", "", "text(*.txt)", options = options)
        print(files)

    def saveFile(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "untitled.txt", "All Text Files")
        print(name)
    
    def addUrl(self):
        index = self.urlsTW.rowCount() + 1
        self.urlsTW.setRowCount(index)
        item = QtWidgets.QTableWidgetItem("")
        self.urlsTW.setItem(index, 0, item)
    
    def removeUrl(self):
        indices = [i.row() for i in self.urlsTW.selectionModel().selectedRows()]
        indices.reverse()
        for i in indices:
            self.urlsTW.removeRow(i)
    
    def actionNode(self):
        levels = 0
        if self.tree.getLevelItems(self.tree.maxLevel) == []:
            levels = self.tree.maxLevel + 1
        else:
            levels = self.tree.maxLevel + 2
        attribute = self.dialogbox.getAction(levels)
        if attribute != None:
            self.tree.createNode("Action", attribute)
    
    def inputNode(self):
        levels = 0
        if self.tree.getLevelItems(self.tree.maxLevel) == []:
            levels = self.tree.maxLevel + 1
        else:
            levels = self.tree.maxLevel + 2
        attribute = self.dialogbox.getInput(levels)
        if attribute != None:
            self.tree.createNode("Input", attribute)
    
    def dataNode(self):
        levels = 0
        if self.tree.getLevelItems(self.tree.maxLevel) == []:
            levels = self.tree.maxLevel + 1
        else:
            levels = self.tree.maxLevel + 2
        attribute = self.dialogbox.getData(levels)
        if attribute != None:
            self.tree.createNode("Data", attribute)
    
    def connectNode(self):
        if self.connect_flag:
            self.tree.enableLabel(False)
            self.connect_flag = False
        else:
            self.tree.enableLabel(True)
            self.connect_flag = True
            self.treeF.connecterdown()
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Control and self.connect_flag:
            self.tree.ctrl_flag = False
            self.treeF.ctrl_flag = False
        elif event.key() == QtCore.Qt.Key_Delete and self.connect_flag:
            self.tree.removeNode()
    
    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Control:
            self.tree.ctrl_flag = True
            self.treeF.ctrl_flag = True
            self.tree.ctrlOff(False)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
