from utils import readObject
from constants import ACTION_TYPE, INITIAL_DIRECTORY, TXT_FILE_FILTER
import os

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QTableWidgetItem

from Interface.UI_AutomScra import Ui_MainWindow
from Structure.DialogBox import DialogBox
from Structure.Frame import Frame
from Structure.ProgressView import ProgressView
from Structure.SaveDB import SaveDB
from Structure.Tree import Tree
from Structure.UrlFeed import UrlFeed


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        '''
        Main Window
        '''
        # Setup UI design
        super(Window, self).__init__()
        self.setupUi(self)

        # Property variable
        self.url: str = None
        # self.saveDatato = None
        # self.saveto = None
        # self.progress = 0
        self.file: str = None
        self.title: str = "Untitled"
        # Flag variable
        self.save_flag: bool = False
        self.empty_flag: bool = True
        self.connect_flag: bool = True

        self.setWindowTitle(self.title + " - AutomScra")
        self.treeF = Frame(self)
        self.treeF.setFixedSize(579, 555)
        self.treeSA.setWidget(self.treeF)
        self.intialheight = self.size().height()
        self.intialwidth = self.size().width()
        self.tree = Tree(self.treeF, self.treeF.size().width(), self.treeF.size().height())

        # Connecting function to button and menu item
        self.actionNew.triggered.connect(self.newFile)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionExit.triggered.connect(self.close)
        self.actionUrls.triggered.connect(self.importUrls)
        self.actionsaveExcel.triggered.connect(self.savetoExcel)
        self.actionsaveDB.triggered.connect(self.savetoDB)
        self.addUrlPB.clicked.connect(self.addUrl)
        self.removeUrlPB.clicked.connect(self.removeUrl)
        self.action_nodePB.clicked.connect(self.actionNode)
        self.input_nodePB.clicked.connect(self.inputNode)
        self.data_nodePB.clicked.connect(self.dataNode)
        self.connectorPB.clicked.connect(self.connectNode)
        self.executePB.clicked.connect(self.executeScript)
        self.urlsTW.itemChanged.connect(self.performUnsaved)

    def actionNode(self):
        levels = 0
        if self.tree.getLevelItems(self.tree.maxLevel) == []:
            levels = self.tree.maxLevel + 1
        else:
            levels = self.tree.maxLevel + 2
        attribute = DialogBox.getAction(self, levels)
        if attribute != None:
            self.tree.createNode(ACTION_TYPE, attribute)
            self.performUnsaved()
    
    def performUnsaved(self):
        self.setWindowTitle("*" + self.windowTitle())
        self.save_flag = True
        self.empty_flag = False

    def addUrl(self, url=""):
        index = self.urlsTW.rowCount() + 1
        self.urlsTW.setRowCount(index)
        self.urlsTW.setItem(index - 1, 0, QTableWidgetItem(url))

    def closeEvent(self, event):
        if self.save_flag:
            reply = QMessageBox.question(
                self, 
                "AutomScra", 
                "Do you want to save changes to " + self.title,
                QMessageBox.Discard | QMessageBox.Cancel | QMessageBox.Save, QMessageBox.Cancel
            )
            if reply == QMessageBox.Save:
                self.saveFile()
                event.accept()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()
                self.keyReleaseEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_Control, Qt.NoModifier, 0, 0, 0))
        else:
            event.accept()

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
        attribute = DialogBox.getData(self, levels)
        if attribute != None:
            self.tree.createNode("Data", attribute)
            self.performUnsaved()

    def executeScript(self):
        if self.save_flag:
            reply = QMessageBox.question(
                self, "Alert", "File is not saved.", QMessageBox.Cancel | QMessageBox.Save, QMessageBox.Cancel)
            if reply == QMessageBox.Save:
                self.saveFile()
            else:
                return None
        if self.progress == 100:
            reply = QMessageBox.question(
                self, "Alert", "Do you want to  execute again.", QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.progress = 0
                self.save_flag = True
            else:
                return None
        path_list, header = self.tree.getAllPath()
        url_list = []
        for i in range(self.urlsTW.rowCount()):
            url = self.urlsTW.item(i, 0).text().lower()
            if url == "":
                continue
            if url.startswith("http://") or url.startswith("https://"):
                url_list.append(self.urlsTW.item(i, 0).text())
            else:
                url_list.append("http://" + self.urlsTW.item(i, 0).text())
        if url_list == []:
            QMessageBox.warning(self, 'Alert', "URL bin is empty.")
        elif self.saveDatato == None:
            QMessageBox.warning(
                self, "Alert", "Location and mode for data saving is not selected")
        elif path_list != []:
            progressview = ProgressView(
                self, path_list, url_list, self.saveDatato, header, self.progress)
            progress = progressview.run()
            if progress != None and progress != self.progress:
                self.progress = progress
                self.save_flag = True

    def getStat(self):
        stat = {}
        stat['frame'] = self.treeF.getStat()
        stat['progress'] = self.progress
        stat['saveDatato'] = self.saveDatato
        stat['tree'] = self.tree.getStat()
        stat['urls'] = []
        for i in range(self.urlsTW.rowCount()):
            stat['urls'].append(self.urlsTW.item(i, 0).text())
        return stat

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
        attribute = DialogBox.getInput(self, levels)
        if attribute != None:
            self.tree.createNode("Input", attribute)
            self.performUnsaved()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control and self.connect_flag:
            self.tree.ctrl_flag = False
            self.treeF.ctrl_flag = False
        elif event.key() == Qt.Key_Delete and self.connect_flag:
            self.tree.removeNode()
            self.treeF.delete()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.tree.ctrl_flag = True
            self.treeF.ctrl_flag = True
            self.tree.ctrlOff(False)

    def newFile(self):
        if not self.empty_flag:
            window = Window()
            window.show()
        self.keyReleaseEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_Control, Qt.NoModifier, 0, 0, 0))

    def openFile(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open", INITIAL_DIRECTORY, TXT_FILE_FILTER)
        if file == '':
            return
        
        if self.empty_flag:
            self.setStat(file)
        else:
            window = Window(file)
            window.show()
        self.keyReleaseEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_Control, Qt.NoModifier, 0, 0, 0))

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
        if self.saveto == None:
            files, _ = QFileDialog.getSaveFileName(
                self, "Save File", self.title, "Text Files(*.txt)")
            if files == '':
                return None
            if self.controller.check('defaulter_files', files):
                QMessageBox.warning(self, 'Alert', "File is already open.")
                return None
            self.saveto = os.path.splitext(files)[0] + '.txt'
            self.setWindowTitle(os.path.split(self.saveto)[1] + '- AutomScra')
            self.controller.setValue('reusable_titles', self.title)
            self.controller.setValue('defaulter_files', self.saveto)
            self.save_flag = True
            self.empty_flag = False
        if not self.save_flag:
            return None
        with open(self.saveto, 'w', encoding='utf-8') as fle:
            json.dump(self.getStat(), fle, ensure_ascii=False, indent=4)
        self.save_flag = False
        self.keyReleaseEvent(
            QKeyEvent(QEvent.KeyPress, Qt.Key_Control, Qt.NoModifier, 0, 0, 0))

    def savetoDB(self):
        savedb = None
        if self.saveto != None and self.saveto[0]:
            savedb = SaveDB(self, self.saveto[1], self.saveto[2])
        else:
            savedb = SaveDB(self)
        attrs = savedb.run()
        if attrs != None:
            self.saveto = [1] + attrs
            self.save_flag = True
            self.empty_flag = False

    def savetoExcel(self):
        name = ""
        if self.saveto != None and not self.saveto[0]:
            name, _ = QFileDialog.getSaveFileName(
                self, "Save Data to", self.saveto[1], "Excel(*.xlsx)")
        else:
            name, _ = QFileDialog.getSaveFileName(
                self, "Save Data to", "untitled.xlsx", "Excel(*.xlsx)")
        if name != "":
            self.saveDatato = [0, name]
            self.save_flag = True
            self.empty_flag = False

    def setStat(self, files):
        try:
            stat = None
            with open(files, 'r', encoding='utf-8') as fle:
                stat = json.load(fle)
            self.treeF.setStat(stat['frame'])
            self.progress = stat['progress']
            self.saveDatato = stat['saveDatato']
            self.tree.setStat(stat['tree'])
            for url in stat['urls']:
                self.addUrl(url)
            self.save_flag = False
            self.saveto = files
            self.setWindowTitle(os.path.split(self.saveto)[1] + '- AutomScra')
        except:
            QMessageBox.warning(
                self, 'Alert', "File is corrupted or does not exist.")
            self.saveto = files
            self.close()
