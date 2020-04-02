import datetime

from PyQt5 import QtCore, QtGui, QtWidgets


class Label(QtWidgets.QLabel):
    def __init__(self, args):
        self.tree = args[1]
        self.border_flag = True
        self.conn_flag = True
        self.ctrl_signal = True
        self.parents = []
        self.childs = []
        self.method = args[5]
        self.level = args[6]
        self.attribute = args[7:]
        self.order = datetime.datetime.now()

        QtWidgets.QLabel.__init__(self, parent=args[0])
        self.setGeometry(QtCore.QRect(args[3], args[4], 40, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.setFont(font)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setObjectName(args[2])
        self.setText(args[2])
        self.setStyleSheet("border: 1px solid #000000; border-radius: 5%;")

        self.menu = QtWidgets.QMenu(self)
        self.menu.setStyleSheet("""
            QMenu::item {
                background-color: #ffffff;
                color: #000000;
            }
            QMenu::item:selected {
                background-color: #308cc6;
                color: #ffffff;
            }
        """)

        changeA = QtWidgets.QAction('Change property', self)
        changeA.triggered.connect(self.mouseDoubleClickEvent)
        self.menu.addAction(changeA)

        deleteA = QtWidgets.QAction('Delete node', self)
        deleteA.setShortcut("Del")
        deleteA.triggered.connect(self.tree.removeNode)
        self.menu.addAction(deleteA)
        self.show()

    def clear(self):
        self.setStyleSheet("background: #EFEFEF; color: #000000;border: 1px solid #000000; border-radius: 5%;")
        self.border_flag = True

    def contextMenuEvent(self, event):
        if self.conn_flag:
            self.menu.popup(QtGui.QCursor.pos())

    def getStat(self):
        stat = {}
        stat['args'] = [self.text(), self.pos().x(), self.pos().y(), self.method, self.level] + self.attribute
        stat['childs'] = self.childs
        stat['parents'] = self.parents
        stat['order'] = str(self.order)
        return stat

    def mouseDoubleClickEvent(self, event):
        if self.conn_flag:
            self.tree.changeNode(self.text())

    def mousePressEvent(self, event):
        if not self.conn_flag:
            self.parent().indicateLabel(self.objectName(), self.pos())
        self.tree.clearSelection(self.text())
        if self.border_flag or event.button() == QtCore.Qt.RightButton or not self.conn_flag or not self.ctrl_signal:
            self.setStyleSheet("background: #565656; color: #EFEFEF; border-radius: 5%;")
            self.border_flag = False
            self.tree.ctrlOff(True)
        else:
            self.setStyleSheet("border: 1px solid #000000; border-radius: 5%;")
            self.border_flag = True
