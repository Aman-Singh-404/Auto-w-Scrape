"""
Label widget and it's method
"""

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtWidgets import QAction, QFrame, QLabel, QMenu
from src.model.node import Node


class Label(QLabel):
    """
    Label Widget
    """

    def __init__(self, parent: QFrame, node: Node, pos_x: int, pos_y: int):
        # Setup UI design
        QLabel.__init__(self, parent=parent)
        self.setGeometry(QRect(pos_x, pos_y, 40, 40))
        font = QFont()
        font.setPointSize(14)
        self.setFont(font)
        self.setAlignment(Qt.AlignCenter)
        self.setObjectName(node.name)
        self.setText(node.name)
        self.setStyleSheet("border: 1px solid #000000; border-radius: 5%;")

        # Property variables
        self.parents: list = []  # Store all parents of node
        self.childs: list = []  # Store all children of node
        self.node: Node = node  # Store node attrbutes
        self.border_flag = True
        self.conn_flag = True
        self.ctrl_signal = True

        # Setting Context Menu & style for label
        self.menu = QMenu(self)
        # Menu for changing label attributes
        action_change = QAction("Change property", self)
        action_change.triggered.connect(self.mouseDoubleClickEvent)
        self.menu.addAction(action_change)

        # Menu for deleting label
        action_delete = QAction("Delete node", self)
        action_delete.setShortcut("Del")
        action_delete.triggered.connect(self.parent().tree.removeNode)
        self.menu.addAction(action_delete)

        # Menu Stylesheet
        self.menu.setStyleSheet(
            """
            QMenu::item {
                background-color: #ffffff;
                color: #000000;
            }
            QMenu::item:selected {
                background-color: #308cc6;
                color: #ffffff;
            }
            """
        )
        self.show()

    def clear(self) -> None:
        """
        Clear style of label and set defaults
        """
        self.setStyleSheet(
            "background: #EFEFEF; color: #000000; border: 1px solid #000000; border-radius: 5%;"
        )
        self.border_flag = True

    def contextMenuEvent(self, event) -> None:
        """
        Control menu popup
        """
        if self.conn_flag:
            self.menu.popup(QCursor.pos())

    def store(self) -> dict:
        """
        Load label
        """
        # Attributes of node
        node_attr: dict = {}
        node_attr["order"] = self.node.name
        node_attr["order"] = self.node.value
        node_attr["order"] = self.node.node_type
        node_attr["order"] = self.node.level
        node_attr["order"] = self.node.inner_type
        node_attr["order"] = self.node.order

        # Attributes of label
        label_attr: dict = {}
        label_attr["node"] = node_attr
        label_attr["pos_x"] = self.pos().x()
        label_attr["pos_y"] = self.pos().y()
        label_attr["childs"] = self.childs
        label_attr["parents"] = self.parents

        return label_attr

    def mouseDoubleClickEvent(self, event) -> None:
        """
        Control label double click
        """
        if self.conn_flag:
            self.parent().updateNode(self.text())

    def mousePressEvent(self, event) -> None:
        """
        Control label click
        """
        # clear all selection of labels
        self.parent().tree.clearSelection(self.text())
        if not self.conn_flag:
            self.parent().indicateLabel(self.objectName(), self.pos())
        if (
            self.border_flag
            or event.button() == Qt.RightButton
            or not self.conn_flag
            or not self.ctrl_signal
        ):
            # Set style as selected label
            self.setStyleSheet(
                "background: #565656; color: #EFEFEF; border-radius: 5%;"
            )
            self.border_flag = False
            self.parent().tree.ctrlOff(True)
        else:
            # Set style to default
            self.setStyleSheet("border: 1px solid #000000; border-radius: 5%")
            self.border_flag = True
