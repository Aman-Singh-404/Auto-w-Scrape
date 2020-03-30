from PyQt5 import QtCore, QtGui


class Connector(QtCore.QRect):
    def __init__(self, inherit, pos):
        self.text = ""
        self.line = None
        self.connectedEnds = []
        self.selected = True

        QtCore.QRect.__init__(self)
        if inherit == "parent":
            self.text = "P"
            self.line = QtCore.QLine(
                pos.x() + 20, pos.y() - 10, pos.x() + 20, pos.y())
            self.setRect(pos.x() + 10, pos.y() - 30, 20, 20)
        else:
            self.text = "C"
            self.line = QtCore.QLine(
                pos.x() + 20, pos.y() + 40, pos.x() + 20, pos.y() + 50)
            self.setRect(pos.x() + 10, pos.y() + 50, 20, 20)

    def drawConnector(self, painter):
        painter.setPen(QtCore.Qt.black)
        font = QtGui.QFont()
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawLine(self.line)
        if self.selected:
            painter.setBrush(QtCore.Qt.black)
            painter.drawEllipse(self)
            painter.setPen(QtCore.Qt.white)
            painter.drawText(self, QtCore.Qt.AlignHCenter |
                             QtCore.Qt.AlignVCenter, self.text)
        else:
            painter.setBrush(QtCore.Qt.white)
            painter.drawEllipse(self)
            painter.setPen(QtCore.Qt.black)
            painter.drawText(self, QtCore.Qt.AlignHCenter |
                             QtCore.Qt.AlignVCenter, self.text)

    def updateConnector(self, pos):
        if self.text == "P":
            self.line = QtCore.QLine(
                pos.x() + 20, pos.y() - 10, pos.x() + 20, pos.y())
            self.setRect(pos.x() + 10, pos.y() - 30, 20, 20)
        else:
            self.line = QtCore.QLine(
                pos.x() + 20, pos.y() + 40, pos.x() + 20, pos.y() + 50)
            self.setRect(pos.x() + 10, pos.y() + 50, 20, 20)
