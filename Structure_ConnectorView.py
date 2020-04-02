from PyQt5 import QtCore, QtGui, QtWidgets

from UI_connectorView import Ui_Dialog


class ConnectorView(QtWidgets.QDialog):
    def __init__(self, parent, conn_list):
        self.connector = {}
        self.label = 40
        self.spacing = 10
        self.delete_items = []

        QtWidgets.QDialog.__init__(self, parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())

        self.spanF = QtWidgets.QFrame(self)
        self.spanF.setFixedSize(self.ui.spanSA.size().width(), 60)
        self.ui.spanSA.setWidget(self.spanF)

        for i in range(len(conn_list)):
            self.addConnector(conn_list[i], i)

        self.ui.cancelPB.clicked.connect(self.reject)
        self.ui.deletePB.clicked.connect(self.delete)
        self.ui.selectPB.clicked.connect(self.select)

    def addConnector(self, name, x):
        label = QtWidgets.QLabel(parent=self.spanF)
        x = (self.label + self.spacing) * x + self.spacing
        if x + self.label + self.spacing > self.spanF.size().width():
            self.spanF.setFixedSize(x + self.label + self.spacing, self.spanF.size().height())
        label.setGeometry(QtCore.QRect(x, 10, self.label, self.label))
        font = QtGui.QFont()
        font.setPointSize(14)
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setObjectName(name)
        label.setText(name)
        label.setStyleSheet("border: 1px solid #000000; border-radius: 5%;")
        self.connector[name] = [label, True]

    def delete(self):
        for key, [value, flag] in self.connector.items():
            if not flag:
                self.delete_items.append(key)
        self.accept()

    def mousePressEvent(self, event):
        all_True = "Deselect All"
        for key, [value, flag] in self.connector.items():
            if QtCore.QRect(value.pos(), QtCore.QSize(40, 40)).contains(event.pos()):
                if flag:
                    value.setStyleSheet("background: #565656; color: #EFEFEF; border-radius: 5%;")
                else:
                    value.setStyleSheet("border: 1px solid #000000; border-radius: 5%;")
                    all_True = "Select All"
                self.connector[key][1] = not flag
            else:
                if flag:
                    all_True = "Select All"
        self.ui.selectPB.setText(all_True)

    def run(self):
        if self.exec_():
            return self.delete_items
        self.show()

    def select(self):
        text = ""
        for key, [value, flag] in self.connector.items():
            if self.ui.selectPB.text() == "Select All":
                value.setStyleSheet("background: #565656; color: #EFEFEF; border-radius: 5%;")
                text = "Deselect All"
                self.connector[key][1] = False
            else:
                value.setStyleSheet("border: 1px solid #000000; border-radius: 5%;")
                text = "Select All"
                self.connector[key][1] = True
        self.ui.selectPB.setText(text)
