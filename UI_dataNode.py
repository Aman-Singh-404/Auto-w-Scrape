# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/aman/Desktop/AutomScra/dataNode.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 130)
        Dialog.setMinimumSize(QtCore.QSize(350, 130))
        Dialog.setMaximumSize(QtCore.QSize(350, 130))
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(5, 95, 340, 35))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_1 = QtWidgets.QLabel(Dialog)
        self.label_1.setGeometry(QtCore.QRect(5, 5, 75, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(5, 35, 75, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(5, 65, 75, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.levelCB = QtWidgets.QComboBox(Dialog)
        self.levelCB.setGeometry(QtCore.QRect(85, 5, 260, 30))
        self.levelCB.setObjectName("levelCB")
        self.actionCB = QtWidgets.QComboBox(Dialog)
        self.actionCB.setGeometry(QtCore.QRect(85, 35, 260, 30))
        self.actionCB.setObjectName("actionCB")
        self.actionCB.addItem("")
        self.actionCB.addItem("")
        self.valueLE = QtWidgets.QLineEdit(Dialog)
        self.valueLE.setGeometry(QtCore.QRect(85, 65, 260, 30))
        self.valueLE.setObjectName("valueLE")

        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.accepted.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Data Node"))
        self.label_1.setText(_translate("Dialog", "Level:"))
        self.label_2.setText(_translate("Dialog", "Type"))
        self.label_3.setText(_translate("Dialog", "Value:"))
        self.actionCB.setItemText(0, _translate("Dialog", "Text"))
        self.actionCB.setItemText(1, _translate("Dialog", "Media"))
