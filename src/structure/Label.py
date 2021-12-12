import datetime

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtWidgets import QAction, QLabel, QMenu


class Label(QLabel):
    def __init__(self, args):

        # {'level': 0, 'action_type': <Action_Type.Click: 1>, 'value': '<a>', 
        # 'frame': <src.structure.Frame.Frame object at 0x000001B79B4BD900>, 
        # 'tree': <src.model.Tree.Tree object at 0x000001B79B530580>, 
        # 'node_type': <Action_Type.Click: 1>, 'name': 'A1', 'pos_x': 10, 'pos_y': 10}
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

        QLabel.__init__(self, parent=args[0])
        self.setGeometry(QRect(args[3], args[4], 40, 40))
        font = QFont()
        font.setPointSize(14)
        self.setFont(font)
        self.setAlignment(Qt.AlignCenter)
        self.setObjectName(args[2])
        self.setText(args[2])
        self.setStyleSheet("border: 1px solid #000000 border-radius: 5%")

        self.menu = QMenu(self)
        self.menu.setStyleSheet("""
            QMenu::item {
                background-color: #ffffff
                color: #000000
            }
            QMenu::item:selected {
                background-color: #308cc6
                color: #ffffff
            }
        """)

        changeA = QAction('Change property', self)
        changeA.triggered.connect(self.mouseDoubleClickEvent)
        self.menu.addAction(changeA)

        deleteA = QAction('Delete node', self)
        deleteA.setShortcut("Del")
        deleteA.triggered.connect(self.tree.removeNode)
        self.menu.addAction(deleteA)
        self.show()

    def clear(self):
        self.setStyleSheet("background: #EFEFEF color: #000000border: 1px solid #000000 border-radius: 5%")
        self.border_flag = True

    def contextMenuEvent(self, event):
        if self.conn_flag:
            self.menu.popup(QCursor.pos())

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
        if self.border_flag or event.button() == Qt.RightButton or not self.conn_flag or not self.ctrl_signal:
            self.setStyleSheet("background: #565656 color: #EFEFEF border-radius: 5%")
            self.border_flag = False
            self.tree.ctrlOff(True)
        else:
            self.setStyleSheet("border: 1px solid #000000 border-radius: 5%")
            self.border_flag = True
