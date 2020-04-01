from PyQt5 import QtWidgets

from UI_actionNode import Ui_Dialog as actionD


class DialogBox:
    def __init__(self, parent):
        self.parent = parent

    def getAction(self, levels):
        dialog = QtWidgets.QDialog(self.parent)
        dialog.ui = actionD()
        dialog.ui.setupUi(dialog)
        for i in range(levels):
            dialog.ui.levelCB.addItem("Level " + str(i + 1))
        if dialog.exec_():  # and dialog.ui.valueLE.text() != "":
            level = int(
                ''.join(x for x in dialog.ui.levelCB.currentText() if x.isdigit())) - 1
            action = dialog.ui.actionCB.currentText()
            value = dialog.ui.valueLE.text()
            return [level, action, value]
        dialog.show()

    def getData(self, levels):
        dialog = QtWidgets.QDialog(self.parent)
        dialog.ui = actionD()
        dialog.ui.setupUi(dialog, levels)
        if dialog.exec_() and dialog.ui.valueLE.text() != "":
            level = int(
                ''.join(x for x in dialog.ui.levelCB.currentText() if x.isdigit())) - 1
            action = dialog.ui.actionCB.currentText()
            value = dialog.ui.valueLE.text()
            return [level, action, value]
        dialog.show()

    def getInput(self, levels):
        dialog = QtWidgets.QDialog(self.parent)
        dialog.ui = actionD()
        dialog.ui.setupUi(dialog, levels)
        if dialog.exec_() and dialog.ui.valueLE.text() != "":
            level = int(
                ''.join(x for x in dialog.ui.levelCB.currentText() if x.isdigit())) - 1
            action = dialog.ui.actionCB.currentText()
            value = dialog.ui.valueLE.text()
            return [level, action, value]
        dialog.show()
