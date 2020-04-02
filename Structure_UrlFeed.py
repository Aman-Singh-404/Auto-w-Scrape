import os

import pandas as pd
from PyQt5 import QtWidgets

from UI_urlFeed import Ui_Dialog


class UrlFeed(QtWidgets.QDialog):
    def __init__(self, parent):
        self.extension = "Excel/Text csv(*.xlsx *.csv)"
        self.filepath = None
        self.Urls = []

        QtWidgets.QDialog.__init__(self, parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.fileRB.toggled.connect(self.showWidget)
        self.ui.browsePB.clicked.connect(self.openBrowse)
        self.ui.cancelPB.clicked.connect(self.reject)
        self.ui.importPB.clicked.connect(self.importUrls)

        self.ui.label.hide()
        self.ui.separatorLE.hide()
        self.ui.cancelPB.move(210, 90)
        self.ui.importPB.move(320, 90)
        self.setFixedSize(430, 130)

    def importUrls(self):
        if self.filepath == None:
            QtWidgets.QMessageBox.warning(self, 'Alert', "No file selected!")
            return None
        if self.ui.fileRB.isChecked():
            if self.ui.separatorLE.text() == "":
                QtWidgets.QMessageBox.warning(self, 'Alert', "Separator field is empty!")
                return None
            else:
                self.Urls = open(self.filepath, "r").read().replace("\n", "").split(self.ui.separatorLE.text())
                self.Urls = [x for x in self.Urls if x]
        else:
            df = None
            if os.path.splitext(self.filepath)[1] == ".csv":
                df = pd.read_csv(self.filepath, header=None)
            else:
                df = pd.read_excel(self.filepath, header=None)
            self.Urls += list(df[0])
        self.accept()

    def openBrowse(self):
        files, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select file", "", self.extension)
        if files == '':
            return None
        self.filepath = files
        if len(os.path.split(self.filepath)[1]) > 15:
            self.ui.browseL.setText(os.path.split(self.filepath)[1][:15]+"...")
        else:
            self.ui.browseL.setText(os.path.split(self.filepath)[1])

    def run(self):
        if self.exec_():
            return self.Urls
        else:
            return []
        self.show()

    def showWidget(self):
        if self.ui.fileRB.isChecked():
            self.ui.label.show()
            self.ui.separatorLE.show()
            self.ui.cancelPB.move(210, 130)
            self.ui.importPB.move(320, 130)
            self.setFixedSize(430, 170)
            self.extension = "Text File(*.txt)"
            if self.filepath != None:
                self.filepath = None
                self.ui.browseL.setText("")
        else:
            self.ui.label.hide()
            self.ui.separatorLE.hide()
            self.ui.cancelPB.move(210, 90)
            self.ui.importPB.move(320, 90)
            self.setFixedSize(430, 130)
            self.extension = "Excel/Text csv(*.xlsx *.csv)"
            if self.filepath != None:
                self.filepath = None
                self.ui.browseL.setText("")
