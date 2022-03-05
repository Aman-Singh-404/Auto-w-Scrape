import re

from PyQt5.QtWidgets import QDialog, QMessageBox

from Interface.UI_actionNode import Ui_Dialog


class ActionNode(QDialog):
    def __init__(self, parent, levels, level, action, value):
        QDialog.__init__(self, parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())

        for i in range(levels):
            self.ui.levelCB.addItem("Level " + str(i + 1))

        self.ui.levelCB.setCurrentText(level)
        self.ui.actionCB.currentTextChanged.connect(self.change)
        self.ui.actionCB.setCurrentText(action)
        self.ui.valueLE.setText(value)
        self.change("Click")

        self.ui.buttonBox.accepted.connect(self.verify)
        self.ui.buttonBox.rejected.connect(self.reject)

    def change(self, value):
        if value == "Click":
            self.ui.label_3.setText("Tag:")
        else:
            self.ui.label_3.setText("Value:")

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

    def run(self):
        if self.exec_():
            level = int(self.ui.levelCB.currentText()[6:]) - 1
            action = self.ui.actionCB.currentText()
            value = self.ui.valueLE.text()
            return [level, action, value]
        self.show()

    def verify(self):
        value = self.ui.valueLE.text()
        if self.ui.actionCB.currentText() == "Click" and not self.checkHTML(value):
            QMessageBox.warning(self, "Alert", "HTML tag is invalid.")
        elif self.ui.actionCB.currentText() == "Time" and not (
            value.isdigit() and 0 < int(value) < 21
        ):
            QMessageBox.warning(
                self, "Alert", "Time Delay should be numeric and in range 1 to 20."
            )
        else:
            self.accept()
