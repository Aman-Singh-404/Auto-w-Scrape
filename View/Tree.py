import datetime

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QMessageBox

from Structure.Label import Label


class Tree:
    def __init__(self, *args):
        self.frame = args[0]
        self.height = args[1]
        self.width = args[2]
        self.Head = {}
        self.action = 1
        self.input = 1
        self.data = 1
        self.ctrl_flag = True
        self.maxLevel = 0
        self.dialogbox = None

    def adjustTreePosition(self, level, new_ele=True):
        label = 50
        width_spacing = 10
        height_spacing = 60
        level_items = self.getLevelItems(level)
        x = width_spacing
        y = level * (label + height_spacing) + 10
        no_of_ele = len(level_items)

        if new_ele:
            no_of_ele += 1

        if y + label + height_spacing > self.height:
            self.height = y + label + height_spacing

        if (label + width_spacing) * no_of_ele + width_spacing < self.width:
            x = (self.width - (label + width_spacing) * no_of_ele - width_spacing) / 2
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
            if value.level > level:
                value.level -= 1
        if self.maxLevel > 0:
            self.maxLevel -= 1

    def changeNode(self, node):
        levels = 0
        if self.getLevelItems(self.maxLevel) == []:
            levels = self.maxLevel + 1
        else:
            levels = self.maxLevel + 2
        attribute = None
        lbl = self.Head[node]
        if self.Head[node].method == "Action":
            attribute = self.dialogbox.getAction(levels, lbl.level, lbl.attribute[0], lbl.attribute[1])
        elif self.Head[node].method == "Input":
            attribute = self.dialogbox.getInput(levels, lbl.level, lbl.attribute[0], lbl.attribute[1], lbl.attribute[2])
        else:
            attribute = self.dialogbox.getData(levels, lbl.level, lbl.attribute[0], lbl.attribute[1], lbl.attribute[2], lbl.attribute[3])
        if attribute == None:
            return None
        level = self.Head[node].level
        if not self.checkConnector(node, attribute[0]):
            return None
        self.Head[node].level = attribute[0]
        self.Head[node].attribute = attribute[1:]
        if level != attribute[0] and self.getLevelItems(level) == []:
            self.changeLevels(level)
        if self.maxLevel < attribute[0]:
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
        message = "Element has connector(s) in level " + str(level + 1) + ".\nDo you want to update?"
        reply = QMessageBox.question(self.frame, 'Alert', message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
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

    def createNode(self, method, attribute):
        name = ""
        if method == "Action":
            name = "A" + str(self.action)
            self.action += 1
        elif method == "Input":
            name = "I" + str(self.input)
            self.input += 1
        else:
            name = "D" + str(self.data)
            self.data += 1
        x, y = self.adjustTreePosition(attribute[0])
        if self.maxLevel < attribute[0]:
            self.maxLevel += 1
        self.Head[name] = Label([self.frame, self, name, x, y, method] + attribute)
        self.frame.lines[name] = [None, None]

    def ctrlOff(self, flag):
        for key, value in self.Head.items():
            value.ctrl_signal = flag

    def enableLabel(self, flag):
        for key, value in self.Head.items():
            value.setStyleSheet("border: 1px solid rgb(0, 0, 0); border-radius: 5%;")
            value.conn_flag = flag

    def getAllPath(self):
        if self.Head == {}:
            QMessageBox.warning(self.frame, 'Alert', "Frame is empty.")
            return None, []
        header = []
        for key, label in self.Head.items():
            if label.level != 0 and label.parents == []:
                QMessageBox.warning(self.frame, 'Alert', "Some labels have no parents [Excluding Level 1 nodes].")
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
            if value.level == level:
                level_items.append([key, value.order])
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
        stat['action'] = self.action
        stat['data'] = self.data
        stat['head'] = {}
        for label, item in self.Head.items():
            stat['head'][label] = item.getStat()
        stat['input'] = self.input
        stat['maxlevel'] = self.maxLevel
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
            if len(self.getLevelItems(self.Head[key].level)) == 1:
                message = "This is last element of this level.\nDo you want to delete it?"
                reply = QMessageBox.question(self.frame, 'Alert', message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                continue
            self.frame.deleteConnector(key, [value.parents.copy(), value.childs.copy()])
            value.hide()
            self.Head.pop(key)
            if reply != None:
                self.changeLevels(value.level)
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
        treeSA = self.frame.parent().parent()
        if treeSA.size().width() < self.frame.size().width():
            self.width = treeSA.size().width()
        if treeSA.size().height() < self.frame.size().height():
            self.height = treeSA.size().height()
        for i in range(self.maxLevel + 1):
            self.adjustTreePosition(i, False)
        self.frame.mwindow.save_flag = True

    def setStat(self, stat):
        self.action = stat['action']
        self.data = stat['data']
        for label, item in stat['head'].items():
            self.Head[label] = Label([self.frame, self] + item['args'])
            self.Head[label].childs = item['childs']
            self.Head[label].parents = item['parents']
            self.Head[label].order = datetime.datetime.strptime(item['order'], '%Y-%m-%d %H:%M:%S.%f')
        self.input = stat['input']
        self.maxLevel = stat['maxlevel']
        self.setRelativeSize()
