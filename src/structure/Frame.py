from PyQt5.QtCore import QLine, QPoint
from PyQt5.QtGui import QCursor, QPainter
from PyQt5.QtWidgets import QAction, QFrame, QMenu, QMessageBox
from src.model.Tree import Tree
from src.model.enums import ActionType, DataType, InputType, NodeType

from src.model.node import Node
from src.structure.actionwidget import ActionWidget
from src.structure.datawidget import DataWidget
from src.structure.inputwidget import InputWidget
from src.structure.label import Label


class Frame(QFrame, Tree):
    def __init__(self, parent):
        # Setup UI design
        QFrame.__init__(self, parent=parent)
        self.ctrl_flag = True
        self.state = 0
        self.label = ""
        self.lbl_pos = None
        self.current_conn = None
        self.lines = {}
        self.move_line = QLine()
        self.setMouseTracking(True)

        self.menu = QMenu(self)

        clearA = QAction("Clear Connectors", self)
        clearA.triggered.connect(self.removeAll)
        self.menu.addAction(clearA)

        clearallA = QAction("Clear Frame", self)
        clearallA.triggered.connect(self.clearAll)
        self.menu.addAction(clearallA)

        self.show()

    def adjustTree(self):
        for i in range(self.maxLevel + 1):
            self.adjustTreePosition(i, False)

    def createActionWidget(self):
        """
        Create Action Label
        """
        # Run ActionWidget to get node attribute
        node_attr: dict = ActionWidget(
            self, self.maxLevel + 1, 0, ActionType.CLICK, ""
        ).run()

        if node_attr != {}:
            # If node attributes provided correctly, then create label
            node_attr.update(self.createNode(NodeType.ACTION, node_attr["level"]))
            node: Node = Node(
                node_attr["name"],
                node_attr["value"],
                NodeType.ACTION,
                node_attr["level"],
                node_attr["action_type"],
            )

            # Update Frame by adding Label
            self.Head[node_attr["name"]] = Label(
                self, node, node_attr["pos_x"], node_attr["pos_y"]
            )
            self.lines[node_attr["name"]] = [None, None]

    def createInputWidget(self):
        """
        Create Input Label
        """
        # Run InputWidget to get node attribute
        node_attr: dict = InputWidget(
            self, self.maxLevel + 1, 0, InputType.TEXT, "", ""
        ).run()

        if node_attr != {}:
            # If node attributes provided correctly, then create label
            node_attr.update(self.createNode(NodeType.INPUT, node_attr["level"]))
            node: Node = Node(
                node_attr["name"],
                node_attr["value"],
                NodeType.INPUT,
                node_attr["level"],
                node_attr["input_type"],
            )
            node.setAttribute("input", node_attr["input"])

            # Update Frame by adding Label
            self.Head[node_attr["name"]] = Label(
                self, node, node_attr["pos_x"], node_attr["pos_y"]
            )
            self.lines[node_attr["name"]] = [None, None]

    def createDataWidget(self):
        """
        Create Data Label
        """
        # Run DataWidget to get node attribute
        node_attr: dict = DataWidget(
            self, self.maxLevel + 1, 0, DataType.TEXT, ""
        ).run()

        if node_attr != {}:
            # If node attributes provided correctly, then create label
            node_attr.update(self.createNode(NodeType.INPUT, node_attr["level"]))
            node: Node = Node(
                node_attr["name"],
                node_attr["value"],
                NodeType.DATA,
                node_attr["level"],
                node_attr["input_type"],
            )

            # Update Frame by adding Label
            self.Head[node_attr["name"]] = Label(
                self, node, node_attr["pos_x"], node_attr["pos_y"]
            )
            self.lines[node_attr["name"]] = [None, None]

    def updateNode(self, current_label: Label):
        """
        Used to change attrbutes of label
        """
        node: Node = current_label.node
        node_attr: dict = {}

        # To get updated attributes for node
        if node.node_type == NodeType.ACTION:
            # If node is action type
            node_attr = ActionWidget(
                self, self.maxLevel + 1, node.level, node.inner_type, node.value
            ).run()
        elif node.node_type == NodeType.INPUT:
            # If node is input type
            node_attr = InputWidget(
                self,
                self.maxLevel + 1,
                node.level,
                node.inner_type,
                node.value,
                node.getAttribute("input"),
            ).run()
        else:
            # If node is data type
            node_attr = DataWidget(
                self, self.maxLevel + 1, node.level, node.inner_type, node.value
            ).run()

        # Check whether node attributes has not been updated,
        # Or
        # Connection is violated in parent or child relation
        # Then end
        if node_attr == {} or (
            node.level != node_attr["level"]
            and not self.checkConnection(node, node_attr["level"])
        ):
            return None

        current_label.node.name = node_attr["name"]
        current_label.node.value = node_attr["value"]
        current_label.node.node_type = node_attr["node_type"]
        current_label.node.level = node_attr["level"]
        current_label.node.inner_type = node_attr["inner_type"]
        self.updateTree()

        if node.node_type == NodeType.INPUT:
            # If node is input type, update input attribute
            current_label.node.setAttribute("input", node_attr["input"])
        elif node.node_type == NodeType.DATA:
            # If node is data type, update
            pass

    def clearAll(self):
        self.parent().save_flag = True
        self.removeAll()
        self.parent().tree.removeAllNode()

    def connecterdown(self):
        if self.state == 1:
            self.lines[self.label][1] = None
            self.state = 0
            self.update()

    def connectorSelection(self, pos):
        select = None
        state = None
        for key, conn in self.lines.items():
            if conn[0] != None:
                if conn[0].contains(pos):
                    if self.current_conn == key:
                        conn[0].selected = not conn[0].selected
                    else:
                        conn[0].selected = False
                        self.current_conn = key
                    select = key
                    state = 0
                elif not conn[0].contains(pos) or label:
                    conn[0].selected = True
            if conn[1] != None:
                if conn[1].contains(pos):
                    if self.current_conn == key:
                        conn[1].selected = not conn[1].selected
                    else:
                        conn[1].selected = False
                        self.current_conn = key
                    select = key
                    state = 1
                elif not conn[1].contains(pos) or label:
                    conn[1].selected = True
        if select == None:
            self.update()
            self.current_conn = None
            return None, None, None
        for item in self.lines[select][state].connectedEnds:
            self.lines[item][int(not state)].selected = self.lines[select][
                state
            ].selected
        self.update()
        return select, state, self.lines[select][state].connectedEnds

    def contextMenuEvent(self, event):
        if self.parent().connect_flag:
            self.menu.popup(QCursor.pos())

    def delete(self):
        if self.current_conn != None:
            if (
                self.lines[self.current_conn][0] != None
                and not self.lines[self.current_conn][0].selected
            ):
                self.deleteConnector(
                    self.current_conn,
                    [self.lines[self.current_conn][0].connectedEnds.copy(), []],
                )
            elif (
                self.lines[self.current_conn][1] != None
                and not self.lines[self.current_conn][1].selected
            ):
                self.deleteConnector(
                    self.current_conn,
                    [[], self.lines[self.current_conn][1].connectedEnds.copy()],
                )
            self.current_conn = None

    def deleteConnector(self, label, faulter):
        for item in faulter[0]:
            self.lines[label][0].connectedEnds.remove(item)
            self.lines[item][1].connectedEnds.remove(label)
            self.parent().tree.removeRelations(item, label)
            if self.lines[item][1].connectedEnds == []:
                self.lines[item][1] = None
        if faulter[0] != [] and self.lines[label][0].connectedEnds == []:
            self.lines[label][0] = None
        for item in faulter[1]:
            self.lines[label][1].connectedEnds.remove(item)
            self.lines[item][0].connectedEnds.remove(label)
            self.parent().tree.removeRelations(label, item)
            if self.lines[item][0].connectedEnds == []:
                self.lines[item][0] = None
        if faulter[1] != [] and self.lines[label][1].connectedEnds == []:
            self.lines[label][1] = None
        self.connectorSelection(QPoint(0, 0))
        self.parent().save_flag = True

    def getStat(self):
        stat = {}
        for label, conn in self.lines.items():
            stat[label] = [None, None]
            if conn[0] != None:
                stat[label][0] = conn[0].getStat()
            if conn[1] != None:
                stat[label][1] = conn[1].getStat()
        return stat

    def indicateLabel(self, label, pos):
        self.state = (self.state + 1) % 3
        if self.state == 1:
            if self.lines[label][1] == None:
                self.lines[label][1] = Connector("child", pos)
            self.label = label
            self.lbl_pos = QPoint(pos.x() + 20, pos.y() + 40)
        elif self.lbl_pos.y() < pos.y():
            if self.lines[label][0] == None:
                self.lines[label][0] = Connector("parent", pos)
            if label not in self.lines[self.label][1].connectedEnds:
                self.lines[self.label][1].connectedEnds.append(label)
                self.lines[label][0].connectedEnds.append(self.label)
                self.parent().tree.setRelations(self.label, label)
                self.parent().save_flag = True
            self.update()
            self.state = (self.state + 1) % 3
            self.label = ""
            self.parent().tree.enableLabel(True)
            self.parent().connect_flag = True
        else:
            self.state = (self.state - 1) % 3
            QMessageBox.warning(
                self, "Alert", "Same or top level connectors are restricted."
            )

    def mouseDoubleClickEvent(self, event):
        if self.ctrl_flag and self.parent().connect_flag:
            label, state, item_list = self.connectorSelection(pos=event.pos())
            if label == None:
                return None
            conn_view = ConnectorView(self, item_list)
            delete_items = conn_view.run()
            if delete_items != None:
                faulter = [[], []]
                faulter[state] = delete_items
                self.deleteConnector(label, faulter)
                self.update()

    def mouseMoveEvent(self, event):
        if self.state == 1:
            self.move_line = QLine(self.lbl_pos, event.pos())
            self.update()
        else:
            self.lbl_pos = event.pos()

    def mousePressEvent(self, event):
        if self.ctrl_flag and self.parent().connect_flag:
            self.clearSelection()
            self.connectorSelection(pos=event.pos())

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        if self.state == 1:
            painter.drawLine(self.move_line)
        for _, conn in self.lines.items():
            if conn[0] != None:
                conn[0].drawConnector(painter)
            if conn[1] != None:
                conn[1].drawConnector(painter)
        painter.end()

    def removeAll(self):
        for key, _ in self.lines.items():
            self.lines[key] = [None, None]
        self.update()
        self.parent().tree.removeAllRelations()
        self.parent().save_flag = True

    def setStat(self, stat):
        for label, conn in stat.items():
            self.lines[label] = [None, None]
            if conn[0] != None:
                self.lines[label][0] = Connector(
                    conn[0]["inherit"], QPoint(conn[0]["pos"][0], conn[0]["pos"][1])
                )
                self.lines[label][0].connectedEnds = conn[0]["connectedEnds"]
            if conn[1] != None:
                self.lines[label][1] = Connector(
                    conn[1]["inherit"], QPoint(conn[1]["pos"][0], conn[1]["pos"][1])
                )
                self.lines[label][1].connectedEnds = conn[1]["connectedEnds"]
        self.update()

    def updateconnector(self, update_list):
        for item in update_list:
            position = self.findChild(Label, item).pos()
            if self.lines[item][0] != None:
                self.lines[item][0].updateConnector(position)
            if self.lines[item][1] != None:
                self.lines[item][1].updateConnector(position)
        self.update()
