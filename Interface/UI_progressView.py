# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/aman/Desktop/AutomScra/Interface/progressView.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(270, 150)
        Dialog.setMinimumSize(QtCore.QSize(270, 150))
        Dialog.setMaximumSize(QtCore.QSize(270, 150))
        self.executePB = QtWidgets.QPushButton(Dialog)
        self.executePB.setGeometry(QtCore.QRect(140, 110, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.executePB.setFont(font)
        self.executePB.setObjectName("executePB")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(5, 5, 260, 95))
        self.label.setLineWidth(1)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.closePB = QtWidgets.QPushButton(Dialog)
        self.closePB.setGeometry(QtCore.QRect(10, 110, 120, 30))
        self.closePB.setObjectName("closePB")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Progress Viewer"))
        self.executePB.setText(_translate("Dialog", "Execute"))
        self.label.setText(_translate("Dialog", "Execution process will take some time. And also it open your browser, so please don\'t interfere in the browser process.\n"
" Do you want to continue?"))
        self.closePB.setText(_translate("Dialog", "Close"))
