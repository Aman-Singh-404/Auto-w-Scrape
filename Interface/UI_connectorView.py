# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Interface/connectorView.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(550, 110)
        self.spanSA = QtWidgets.QScrollArea(Dialog)
        self.spanSA.setGeometry(QtCore.QRect(0, 0, 550, 70))
        self.spanSA.setWidgetResizable(True)
        self.spanSA.setObjectName("spanSA")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 548, 68))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.spanSA.setWidget(self.scrollAreaWidgetContents)
        self.selectPB = QtWidgets.QPushButton(Dialog)
        self.selectPB.setGeometry(QtCore.QRect(70, 75, 150, 30))
        self.selectPB.setObjectName("selectPB")
        self.cancelPB = QtWidgets.QPushButton(Dialog)
        self.cancelPB.setGeometry(QtCore.QRect(230, 75, 150, 30))
        self.cancelPB.setObjectName("cancelPB")
        self.deletePB = QtWidgets.QPushButton(Dialog)
        self.deletePB.setGeometry(QtCore.QRect(390, 75, 150, 30))
        self.deletePB.setObjectName("deletePB")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Connector View"))
        self.selectPB.setText(_translate("Dialog", "Select All"))
        self.cancelPB.setText(_translate("Dialog", "Cancel"))
        self.deletePB.setText(_translate("Dialog", "Delete"))
