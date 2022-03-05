import os
import re

from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

from Interface.UI_dataNode import Ui_Dialog


class DataNode(QDialog):
    def __init__(self, parent, levels, level, file_type, tag, path, all):
        self.path = ""

        QDialog.__init__(self, parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())

        for i in range(levels):
            self.ui.levelCB.addItem("Level " + str(i + 1))

        self.ui.levelCB.setCurrentText(level)
        self.ui.typeCB.setCurrentText(file_type)
        self.ui.typeCB.currentTextChanged.connect(self.changeWindow)
        self.ui.singleRB.setChecked(all)
        self.ui.positionSB.setValue(all)
        self.ui.tagLE.setText(tag)
        self.changeWindow(file_type)
        self.setLabel(path)

        self.ui.browsePB.clicked.connect(self.openBrowse)
        self.ui.buttonBox.accepted.connect(self.verify)
        self.ui.buttonBox.rejected.connect(self.reject)

    def changeWindow(self, value):
        if value == "Text":
            self.ui.browsePB.hide()
            self.ui.browseL.hide()
            self.ui.buttonBox.move(179, 130)
            self.setFixedSize(350, 160)
        else:
            self.ui.browsePB.show()
            self.ui.browseL.show()
            self.ui.buttonBox.move(179, 165)
            self.setFixedSize(350, 195)

    def checkHTML(self, string):
        string = re.findall(r"^\<(.*?)\>", string.strip())
        if len(string) != 1:
            return False
        string = re.findall(r"^(\w+)(.*)", string[0].strip())
        if len(string) != 1:
            return False
        _, string = string[0]
        if string == "":
            return True
        occur = string.count("=")
        cover = re.findall(r"=\s*(.*)", string)
        if occur != 0:
            if cover == [""] or cover[0][0] not in ['"', "'"]:
                return False
            else:
                cover = cover[0][0]
            if occur * 2 != string.count(cover):
                return False
        string = re.findall(r"\s*(\w+)\s*=\s*[\'\"]\s*(.+?)\s*[\'\"]|(\w+)", string)
        for arg0, _, _ in string:
            if arg0 != "":
                occur -= 1
        return not bool(occur)

    def openBrowse(self):
        files = ""
        if self.ui.typeCB.currentText() == "Media":
            files, _ = QFileDialog.getSaveFileName(self, "Select file", self.path)
        else:
            files, _ = QFileDialog.getSaveFileName(
                self, "Select file", self.path, "Excel(*.xlsx)"
            )
        if files != "":
            self.setLabel(files)

    def run(self):
        if self.exec_():
            level = int(self.ui.levelCB.currentText()[6:]) - 1
            file_type = self.ui.typeCB.currentText()
            tag = self.ui.tagLE.text()
            all = 0
            if self.ui.singleRB.isChecked():
                all = self.ui.positionSB.value()
            return [level, file_type, tag, self.path, all]
        self.show()

    def setLabel(self, files):
        self.path = files
        if len(os.path.split(self.path)[1]) > 15:
            self.ui.browseL.setText(os.path.split(self.path)[1][:15] + "...")
        else:
            self.ui.browseL.setText(os.path.split(self.path)[1])

    def verify(self):
        if not self.checkHTML(self.ui.tagLE.text()):
            QMessageBox.warning(self, "Alert", "HTML tag is invalid.")
        elif self.ui.typeCB.currentText() == "Media" and self.path == "":
            QMessageBox.warning(self, "Alert", "No location selected.")
        else:
            self.accept()
