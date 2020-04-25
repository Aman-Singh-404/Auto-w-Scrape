import re

from PyQt5.QtWidgets import QDialog, QMessageBox

from Interface.UI_inputNode import Ui_Dialog


class InputNode(QDialog):
    def __init__(self, parent, levels, level, tag_type, tag, value):
        QDialog.__init__(self, parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())

        for i in range(levels):
            self.ui.levelCB.addItem("Level " + str(i + 1))
        
        self.ui.levelCB.setCurrentText(level)
        self.ui.typeCB.setCurrentText(tag_type)
        self.ui.typeCB.currentTextChanged.connect(self.changeWindow)
        self.ui.tagLE.setText(tag)
        self.ui.valueTE.setText(value)
        self.changeWindow(tag_type)
        
        self.ui.buttonBox.accepted.connect(self.verify)
        self.ui.buttonBox.rejected.connect(self.reject)
    
    def changeWindow(self, value):
        if value == "Text/Combo Box":
            self.ui.label_4.hide()
            self.ui.valueTE.show()
            self.ui.buttonBox.move(179, 150)
            self.setFixedSize(350, 180)
        else:
            self.ui.label_4.hide()
            self.ui.valueTE.hide()
            self.ui.buttonBox.move(179, 100)
            self.setFixedSize(350, 130)
    
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
        if occur != 0 :
            if cover == [''] or cover[0][0] not in ['"', "'"]:
                print("pass")
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
    
    def run(self):
        if self.exec_():
            level = int(self.ui.levelCB.currentText()[1:]) - 1
            tag = self.ui.tagLE.text()
            value = self.ui.valueTE.toPlainText()
            return [level, tag_type, tag, value]
        self.show()

    def verify(self):
        if not self.checkHTML(self.ui.tagLE.text()):
            QMessageBox.warning(self, "Alert", "HTML tag is invalid.")
        elif self.ui.typeCB.currentText() == "Text/Combo Box" and self.ui.valueTE.toPlainText() == "":
            QMessageBox.warning(self, "Alert", "Text box is empty.")
        else:
            self.accept()
