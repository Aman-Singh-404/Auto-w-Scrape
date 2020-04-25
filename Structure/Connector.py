from PyQt5.QtCore import QLine, QRect, Qt
from PyQt5.QtGui import QFont


class Connector(QRect):
    def __init__(self, inherit, pos):
        self.text = ""
        self.line = None
        self.connectedEnds = []
        self.selected = True

        QRect.__init__(self)
        if inherit == "parent":
            self.text = "P"
            self.line = QLine(pos.x() + 20, pos.y() - 10, pos.x() + 20, pos.y())
            self.setRect(pos.x() + 10, pos.y() - 30, 20, 20)
        else:
            self.text = "C"
            self.line = QLine(pos.x() + 20, pos.y() + 40, pos.x() + 20, pos.y() + 50)
            self.setRect(pos.x() + 10, pos.y() + 50, 20, 20)

    def drawConnector(self, painter):
        painter.setPen(Qt.black)
        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawLine(self.line)
        if self.selected:
            painter.setBrush(Qt.black)
            painter.drawEllipse(self)
            painter.setPen(Qt.white)
            painter.drawText(self, Qt.AlignHCenter | Qt.AlignVCenter, self.text)
        else:
            painter.setBrush(Qt.white)
            painter.drawEllipse(self)
            painter.setPen(Qt.black)
            painter.drawText(self, Qt.AlignHCenter | Qt.AlignVCenter, self.text)

    def getStat(self):
        stat = {}
        stat['connectedEnds'] = self.connectedEnds
        if self.text == 'P':
            stat['inherit'] = 'parent'
            stat['pos'] = [self.topLeft().x() - 10, self.topLeft().y() + 30]
        else:
            stat['inherit'] = 'child'
            stat['pos'] = [self.topLeft().x() - 10, self.topLeft().y() - 50]
        return stat

    def updateConnector(self, pos):
        if self.text == "P":
            self.line = QLine(pos.x() + 20, pos.y() - 10, pos.x() + 20, pos.y())
            self.setRect(pos.x() + 10, pos.y() - 30, 20, 20)
        else:
            self.line = QLine(pos.x() + 20, pos.y() + 40, pos.x() + 20, pos.y() + 50)
            self.setRect(pos.x() + 10, pos.y() + 50, 20, 20)
