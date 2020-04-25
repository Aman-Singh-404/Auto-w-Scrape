# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Interface/dataNode.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 160)
        Dialog.setMinimumSize(QtCore.QSize(350, 160))
        Dialog.setMaximumSize(QtCore.QSize(350, 160))
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
        self.typeCB = QtWidgets.QComboBox(Dialog)
        self.typeCB.setGeometry(QtCore.QRect(85, 35, 260, 30))
        self.typeCB.setObjectName("typeCB")
        self.typeCB.addItem("")
        self.typeCB.addItem("")
        self.tagLE = QtWidgets.QLineEdit(Dialog)
        self.tagLE.setGeometry(QtCore.QRect(85, 65, 260, 30))
        self.tagLE.setObjectName("tagLE")
        self.browseL = QtWidgets.QLabel(Dialog)
        self.browseL.setGeometry(QtCore.QRect(120, 95, 150, 30))
        self.browseL.setText("")
        self.browseL.setObjectName("browseL")
        self.browsePB = QtWidgets.QPushButton(Dialog)
        self.browsePB.setGeometry(QtCore.QRect(10, 100, 95, 30))
        self.browsePB.setObjectName("browsePB")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(179, 130, 166, 25))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Data Node"))
        self.label_1.setText(_translate("Dialog", "Level:"))
        self.label_2.setText(_translate("Dialog", "Type"))
        self.label_3.setText(_translate("Dialog", "Tag:"))
        self.typeCB.setItemText(0, _translate("Dialog", "Text"))
        self.typeCB.setItemText(1, _translate("Dialog", "Media"))
        self.browsePB.setText(_translate("Dialog", "Browse"))
