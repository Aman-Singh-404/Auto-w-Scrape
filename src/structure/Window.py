import json
import os
from constants import INITIAL_DIRECTORY, INITIAL_HEIGHT, INITIAL_TITLE, INITIAL_WIDTH, TXT_FILE_FILTER

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import (QFileDialog, QMainWindow, QMessageBox,
                             QTableWidgetItem)
from src.interface.UI_automScra import Ui_MainWindow
from src.model.Tree import Tree
from src.structure.Frame import Frame


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # Setup UI design
        super(Window, self).__init__()
        self.setupUi(self)

        # Property variables
        self.urls: list = []  # Store all urls
        self.location = None  # Store file location
        self.title: str = "Untitled" # Store file title
        # Flag variables
        self.save_flag: bool = False  # True indicates file is unsaved
        self.empty_flag: bool = True  # True indicates frame is empty
        self.connect_flag: bool = True

        # Setting Window Attributes
        self.setWindowTitle(self.title)
        self.frame: Frame = Frame(self)
        self.frame.setFixedSize(INITIAL_WIDTH, INITIAL_HEIGHT)
        self.treeSA.setWidget(self.frame)
        self.intialheight: int = self.size().height()
        self.intialwidth: int = self.size().width()

        # Connecting action widgets to their respective functions
        self.actionNew.triggered.connect(self.newFile)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionExit.triggered.connect(self.close)
        # self.actionsaveExcel.triggered.connect(self.savetoExcel)
        # self.addUrlPB.clicked.connect(self.addUrl)
        # self.removeUrlPB.clicked.connect(self.removeUrl)
        self.action_nodePB.clicked.connect(self.actionNode)
        self.input_nodePB.clicked.connect(self.inputNode)
        self.data_nodePB.clicked.connect(self.dataNode)
        self.connectorPB.clicked.connect(self.connectNode)
        self.executePB.clicked.connect(self.executeScript)
        self.urlsTW.itemChanged.connect(self.performUnsaved)

    def actionNode(self):
        self.frame.createActionWidget()
        self.performUnsaved()

    def performUnsaved(self):
        if not self.save_flag:
            self.setWindowTitle("*" + self.windowTitle())
            self.save_flag = True
            self.empty_flag = False

    def addUrl(self, url=""):
        index = self.urlsTW.rowCount() + 1
        self.urlsTW.setRowCount(index)
        self.urlsTW.setItem(index - 1, 0, QTableWidgetItem(url))

    def closeEvent(self, event):
        '''
        Exit the application
        '''
        if self.save_flag:
            # If Window is unsaved, then ask for saving the information.
            reply = QMessageBox.question(
                self,
                "AutomScra",
                f"Do you want to save changes to {self.title}?",
                QMessageBox.Discard | QMessageBox.Cancel | QMessageBox.Save, QMessageBox.Cancel
            )
            if reply == QMessageBox.Save:
                self.saveFile()
                event.accept()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()
                self.keyReleaseEvent(
                    QKeyEvent(QEvent.KeyPress, Qt.Key_Control, Qt.NoModifier, 0, 0, 0))
        else:
            event.accept()

    def connectNode(self):
        if self.connect_flag:
            # self.tree.enableLabel(False)
            self.connect_flag = False
        else:
            # self.tree.enableLabel(True)
            self.connect_flag = True
            self.frame.connecterdown()

    def dataNode(self):
        self.frame.createDataWidget()
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
        # path_list, header = self.tree.getAllPath()
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
        stat['frame'] = self.frame.getStat()
        stat['progress'] = self.progress
        stat['saveDatato'] = self.saveDatato
        # stat['tree'] = self.tree.getStat()
        stat['urls'] = []
        for i in range(self.urlsTW.rowCount()):
            stat['urls'].append(self.urlsTW.item(i, 0).text())
        return stat

    def importUrls(self):
        urlfeed = UrlFeed(self)
        for url in urlfeed.run():
            self.addUrl(url)

    def inputNode(self):
        self.frame.createInputWidget()
        self.performUnsaved()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control and self.connect_flag:
            # self.tree.ctrl_flag = False
            self.frame.ctrl_flag = False
        elif event.key() == Qt.Key_Delete and self.connect_flag:
            # self.tree.removeNode()
            self.frame.delete()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            # self.tree.ctrl_flag = True
            self.frame.ctrl_flag = True
            # self.tree.ctrlOff(False)

    def newFile(self):
        '''
        Intialize new window.
        '''
        # If Window isn't empty,  create new Window
        if not self.empty_flag:
            window: Window = Window()
            window.show()
        self.keyReleaseEvent(
            QKeyEvent(QEvent.KeyPress, Qt.Key_Control, Qt.NoModifier, 0, 0, 0))

    def openFile(self):
        '''
        Intialize new window for existing file.
        '''
        # Select path of the file
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open", INITIAL_DIRECTORY, TXT_FILE_FILTER)
        if file_path == '':
            return None

        # If frame is empty, open file in itself, else open new window
        if self.empty_flag:
            self.setStat(file_path)
        else:
            window: Window = Window()
            window.setStat(file_path)
            window.show()
        self.keyReleaseEvent(
            QKeyEvent(QEvent.KeyPress, Qt.Key_Control, Qt.NoModifier, 0, 0, 0))

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

        if (self.treeSA.size().width() - self.frame.size().width()) * incrementwidth > 0:
            pass
            # self.tree.width = self.treeSA.size().width()
        if (self.treeSA.size().height() - self.frame.size().height()) * incrementheight > 0:
            pass
            # self.tree.height = self.treeSA.size().height()

        self.frame.adjustTree()

    def saveFile(self):
        '''
        Save current window information.
        '''
        # If window has no location to save, select a path
        if self.location == None:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save", os.path.join(
                INITIAL_DIRECTORY, INITIAL_TITLE), TXT_FILE_FILTER)
            if file_path == '':
                return None

            # Split path into parent and title
            self.location = file_path
            self.title = os.path.splitext(os.path.split(file_path)[1])[0]

            # Setting Window title and flag variable
            self.setWindowTitle(self.title)
            self.save_flag = True
            self.empty_flag = False

        # If save flag is true, it save window information
        if not self.save_flag:
            return None

        # Saving window information to file
        with open(self.location, 'w', encoding='utf-8') as fle:
            json.dump(self.getStat(), fle, ensure_ascii=False, indent=4)
        self.save_flag = False
        self.keyReleaseEvent(
            QKeyEvent(QEvent.KeyPress, Qt.Key_Control, Qt.NoModifier, 0, 0, 0))

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
            self.frame.setStat(stat['frame'])
            self.progress = stat['progress']
            self.saveDatato = stat['saveDatato']
            # self.tree.setStat(stat['tree'])
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
