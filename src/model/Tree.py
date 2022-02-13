import datetime

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QMessageBox

from src.model.enums import ActionType, NodeType
from src.structure.label import Label
from src.structure.actionwidget import ActionWidget


class Tree:
    def __init__(self, *args):
        self.frame = args[0]
        self.height = args[1]
        self.width = args[2]
        self.Head = {}
        self.action_count = 1
        self.input_count = 1
        self.data_count = 1
        self.ctrl_flag = True
        self.maxLevel = 0
        self.dialogbox = None

    def adjustTreePosition(self, level, new_ele=True):
        label = 50
        width_spacing = 10
        height_spacing = 60
        level_items = self.getLevelItems(level)
        x = width_spacing
        y = int(level * (label + height_spacing) + 10)
        no_of_ele = len(level_items)

        if new_ele:
            no_of_ele += 1

        if y + label + height_spacing > self.height:
            self.height = y + label + height_spacing

        if (label + width_spacing) * no_of_ele + width_spacing < self.width:
            x = int(
                (self.width - (label + width_spacing) * no_of_ele - width_spacing) / 2
            )
        else:
            self.width = (label + width_spacing) * no_of_ele + width_spacing

        self.frame.setFixedSize(self.width, self.height)

        for item in level_items:
            self.Head[item].move(x, y)
            x += label + width_spacing
        self.frame.updateconnector(level_items)
        return x, y

    def changeLevels(self, level):
        for key, value in self.Head.items():
            if value.node.level > level:
                value.level -= 1
        if self.maxLevel > 1:
            self.maxLevel -= 1

    def changeNode(self, node):
        levels = 0
        if self.getLevelItems(self.maxLevel) == []:
            levels = self.maxLevel + 1
        else:
            levels = self.maxLevel + 2
        current_label: Label = self.Head[node]
        if self.Head[node].node.node_type == NodeType.ACTION:
            node_attr: dict = ActionWidget(
                self.frame,
                self.maxLevel + 1,
                current_label.node.level,
                current_label.node.inner_type,
                current_label.node.value,
            ).run()
        elif self.Head[node].node.node_type == NodeType.INPUT:
            attribute = self.dialogbox.getInput(
                levels, lbl.level, lbl.attribute[0], lbl.attribute[1], lbl.attribute[2]
            )
        else:
            attribute = self.dialogbox.getData(
                levels,
                lbl.level,
                lbl.attribute[0],
                lbl.attribute[1],
                lbl.attribute[2],
                lbl.attribute[3],
            )
        if node_attr == {} or not self.checkConnector(node, node_attr["level"]):
            return None

        level = self.Head[node].node.level
        self.Head[node].node.level = node_attr["level"]
        # self.Head[node].attribute = attribute[1:]
        if level != node_attr["level"] and self.getLevelItems(level) == []:
            self.changeLevels(level)
        if self.maxLevel < node_attr["level"]:
            self.maxLevel += 1
        self.setRelativeSize()

    def checkConnector(self, label, level):
        faulter = [[], []]
        for item in self.Head[label].parents:
            if self.Head[item].level >= level:
                faulter[0].append(item)
        for item in self.Head[label].childs:
            if self.Head[item].level <= level:
                faulter[1].append(item)
        if faulter == [[], []]:
            return True
        message = (
            "Element has connector(s) in level "
            + str(level + 1)
            + ".\nDo you want to update?"
        )
        reply = QMessageBox.question(
            self.frame,
            "Alert",
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.frame.deleteConnector(label, faulter)
            return True
        else:
            return False

    def clearSelection(self, node=""):
        if node != "":
            self.frame.connectorSelection(QPoint(0, 0))
        if not self.ctrl_flag:
            return None
        for key, value in self.Head.items():
            if node != key:
                value.clear()

    def createNode(self, node_type: NodeType, level: int) -> dict:
        name: str = None
        if node_type == NodeType.ACTION:
            name = f"A{self.action_count}"
            self.action_count += 1
        elif node_type == NodeType.INPUT:
            name = f"I{self.input_count}"
            self.input_count += 1
        else:
            name = f"D{self.data_count}"
            self.data_count += 1
        x, y = self.adjustTreePosition(level)
        if self.maxLevel <= level:
            self.maxLevel += 1
        return {"name": name, "pos_x": x, "pos_y": y}

    def ctrlOff(self, flag):
        for key, value in self.Head.items():
            value.ctrl_signal = flag

    def enableLabel(self, flag):
        for key, value in self.Head.items():
            value.setStyleSheet("border: 1px solid rgb(0, 0, 0) border-radius: 5%")
            value.conn_flag = flag

    def getAllPath(self):
        if self.Head == {}:
            QMessageBox.warning(self.frame, "Alert", "Frame is empty.")
            return None, []
        header = []
        for key, label in self.Head.items():
            if label.level != 0 and label.parents == []:
                QMessageBox.warning(
                    self.frame,
                    "Alert",
                    "Some labels have no parents [Excluding Level 1 nodes].",
                )
                return None, []
            if label.text()[0] == "D":
                header.append(label.text())
        paths = []
        for child in self.getLevelItems(0):
            paths += self.getPaths(child)
        return paths, header

    def getLevelItems(self, level):
        level_items = []
        for key, value in self.Head.items():
            if value.node.level == level:
                level_items.append([key, value.node.order])
        level_items = sorted(level_items, key=lambda element: element[1], reverse=False)
        level_items = [item[0] for item in level_items]
        return level_items

    def getPaths(self, node):
        paths = []
        if self.Head[node].childs == []:
            return [[self.Head[node]]]
        for child in self.Head[node].childs:
            for p in self.getPaths(child):
                paths.append([self.Head[node]] + p)
        return paths

    def getStat(self):
        stat = {}
        stat["action"] = self.action_count
        stat["data"] = self.data_count
        stat["head"] = {}
        for label, item in self.Head.items():
            stat["head"][label] = item.getStat()
        stat["input"] = self.input_count
        stat["maxlevel"] = self.maxLevel
        return stat

    def removeAllNode(self):
        for _, label in self.Head.items():
            label.hide()
        self.Head = {}
        treeSA = self.frame.parent().parent()
        self.width = treeSA.size().width()
        self.height = treeSA.size().height()
        self.frame.resize(treeSA.size())
        self.maxLevel = 0

    def removeAllRelations(self):
        for _, label in self.Head.items():
            label.parents = []
            label.childs = []

    def removeNode(self):
        keys = []
        for key, value in self.Head.items():
            if not value.border_flag:
                keys.append(key)
        for key in keys:
            value = self.Head[key]
            reply = None
            if len(self.getLevelItems(self.Head[key].node.level)) == 1:
                message = (
                    "This is last element of this level.\nDo you want to delete it?"
                )
                reply = QMessageBox.question(
                    self.frame,
                    "Alert",
                    message,
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )
            if reply == QMessageBox.No:
                continue
            self.frame.deleteConnector(key, [value.parents.copy(), value.childs.copy()])
            value.hide()
            self.Head.pop(key)
            if reply != None:
                self.changeLevels(value.node.level)
        self.setRelativeSize()

    def removeRelations(self, parent, child):
        self.Head[child].parents.remove(parent)
        self.Head[parent].childs.remove(child)

    def setFlag(self, flag):
        for key, value in self.Head.items():
            value.ctrl_flag = flag

    def setRelations(self, parent, child):
        self.Head[child].parents.append(parent)
        self.Head[parent].childs.append(child)

    def setRelativeSize(self):
        treeSA = self.frame.parent()
        if treeSA.size().width() < self.frame.size().width():
            self.width = treeSA.size().width()
        if treeSA.size().height() < self.frame.size().height():
            self.height = treeSA.size().height()
        for i in range(self.maxLevel + 1):
            self.adjustTreePosition(i, False)
        self.frame.parent().save_flag = True

    def setStat(self, stat):
        self.action_count = stat["action"]
        self.data_count = stat["data"]
        for label, item in stat["head"].items():
            self.Head[label] = Label([self.frame, self] + item["args"])
            self.Head[label].childs = item["childs"]
            self.Head[label].parents = item["parents"]
            self.Head[label].order = datetime.datetime.strptime(
                item["order"], "%Y-%m-%d %H:%M:%S.%f"
            )
        self.input_count = stat["input"]
        self.maxLevel = stat["maxlevel"]
        self.setRelativeSize()
