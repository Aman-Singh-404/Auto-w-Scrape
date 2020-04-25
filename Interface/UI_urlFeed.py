# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Interface/urlFeed.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(430, 170)
        self.csvRB = QtWidgets.QRadioButton(Dialog)
        self.csvRB.setGeometry(QtCore.QRect(10, 10, 200, 30))
        self.csvRB.setChecked(True)
        self.csvRB.setObjectName("csvRB")
        self.fileRB = QtWidgets.QRadioButton(Dialog)
        self.fileRB.setGeometry(QtCore.QRect(220, 10, 200, 30))
        self.fileRB.setObjectName("fileRB")
        self.browsePB = QtWidgets.QPushButton(Dialog)
        self.browsePB.setGeometry(QtCore.QRect(20, 50, 150, 30))
        self.browsePB.setObjectName("browsePB")
        self.browseL = QtWidgets.QLabel(Dialog)
        self.browseL.setGeometry(QtCore.QRect(180, 50, 150, 30))
        self.browseL.setText("")
        self.browseL.setObjectName("browseL")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 90, 150, 30))
        self.label.setObjectName("label")
        self.separatorLE = QtWidgets.QLineEdit(Dialog)
        self.separatorLE.setGeometry(QtCore.QRect(180, 90, 200, 30))
        self.separatorLE.setObjectName("separatorLE")
        self.importPB = QtWidgets.QPushButton(Dialog)
        self.importPB.setGeometry(QtCore.QRect(320, 130, 100, 30))
        self.importPB.setObjectName("importPB")
        self.cancelPB = QtWidgets.QPushButton(Dialog)
        self.cancelPB.setGeometry(QtCore.QRect(210, 130, 100, 30))
        self.cancelPB.setObjectName("cancelPB")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Url Feed"))
        self.csvRB.setText(_translate("Dialog", "Extract from Excel/csv file"))
        self.fileRB.setText(_translate("Dialog", "Extract from another file"))
        self.browsePB.setText(_translate("Dialog", "Browse"))
        self.label.setText(_translate("Dialog", "Enter separator:"))
        self.importPB.setText(_translate("Dialog", "Import"))
        self.cancelPB.setText(_translate("Dialog", "Cancel"))
