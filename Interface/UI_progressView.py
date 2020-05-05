# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Desktop/AutomScra/Interface/progressView.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(270, 300)
        Dialog.setMinimumSize(QtCore.QSize(270, 150))
        Dialog.setMaximumSize(QtCore.QSize(270, 2005))
        self.executePB = QtWidgets.QPushButton(Dialog)
        self.executePB.setGeometry(QtCore.QRect(140, 100, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.executePB.setFont(font)
        self.executePB.setObjectName("executePB")
        self.label_1 = QtWidgets.QLabel(Dialog)
        self.label_1.setGeometry(QtCore.QRect(5, 5, 260, 85))
        self.label_1.setLineWidth(1)
        self.label_1.setWordWrap(True)
        self.label_1.setObjectName("label_1")
        self.closePB = QtWidgets.QPushButton(Dialog)
        self.closePB.setGeometry(QtCore.QRect(10, 100, 120, 30))
        self.closePB.setObjectName("closePB")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(0, 133, 270, 5))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setEnabled(False)
        self.label_2.setGeometry(QtCore.QRect(5, 135, 260, 40))
        self.label_2.setLineWidth(1)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.progressPB = QtWidgets.QProgressBar(Dialog)
        self.progressPB.setEnabled(False)
        self.progressPB.setGeometry(QtCore.QRect(10, 185, 250, 25))
        self.progressPB.setProperty("value", 0)
        self.progressPB.setObjectName("progressPB")
        self.pausePB = QtWidgets.QPushButton(Dialog)
        self.pausePB.setEnabled(False)
        self.pausePB.setGeometry(QtCore.QRect(10, 220, 120, 30))
        self.pausePB.setObjectName("pausePB")
        self.cancelPB = QtWidgets.QPushButton(Dialog)
        self.cancelPB.setEnabled(False)
        self.cancelPB.setGeometry(QtCore.QRect(140, 220, 120, 30))
        self.cancelPB.setObjectName("cancelPB")
        self.savePB = QtWidgets.QPushButton(Dialog)
        self.savePB.setEnabled(False)
        self.savePB.setGeometry(QtCore.QRect(10, 260, 120, 30))
        self.savePB.setObjectName("savePB")
        self.stopPB = QtWidgets.QPushButton(Dialog)
        self.stopPB.setEnabled(False)
        self.stopPB.setGeometry(QtCore.QRect(140, 260, 120, 30))
        self.stopPB.setObjectName("stopPB")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Progress Viewer"))
        self.executePB.setText(_translate("Dialog", "Execute"))
        self.label_1.setText(_translate("Dialog", "Execution process will take some time. And also it open your browser, so please don\'t interfere in the browser process.\n"
" Do you want to continue?"))
        self.closePB.setText(_translate("Dialog", "Close"))
        self.label_2.setText(_translate("Dialog", "Wait! Process is ongoing...\n"
""))
        self.pausePB.setText(_translate("Dialog", "Pause"))
        self.cancelPB.setText(_translate("Dialog", "Cancel URL"))
        self.savePB.setText(_translate("Dialog", "Save and Stop"))
        self.stopPB.setText(_translate("Dialog", "Stop"))
