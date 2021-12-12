from src.interface.UI_actionNode import Ui_Dialog
from src.model.Node import Node
from PyQt5.QtWidgets import QDialog, QMessageBox, QWidget
from src.model.Enums import Action_Type
from Utils import validHTMLTag


class ActionNode(QDialog):
    def __init__(self, parent: QWidget, level_count: int, current_level: int, 
    node_type: Action_Type, value: str):
        # Setup UI design
        QDialog.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())

        # Add number of levels from 1 to level_count
        for i in range(level_count):
            self.ui.levelCB.addItem(f"Level {i + 1}")
        
        # Setting atributes
        self.ui.levelCB.setCurrentIndex(current_level)
        self.ui.actionCB.setCurrentText(node_type.name)
        self.ui.valueLE.setText(value)
        
        # Connecting function to button
        self.ui.buttonBox.accepted.connect(self.verify)
        self.ui.buttonBox.rejected.connect(self.reject)
    
    
    def run(self):
        if self.exec_():
            node_attr: dict = {}
            node_attr["level"] = int(self.ui.levelCB.currentText()[6:]) - 1
            node_attr["action_type"] = Action_Type(self.ui.actionCB.currentText())
            node_attr["value"] = self.ui.valueLE.text()
            return node_attr
        self.show()

    def verify(self):
        value = self.ui.valueLE.text()
        if ((self.ui.actionCB.currentText() == Action_Type.Click.name and validHTMLTag(value)) or 
        (self.ui.actionCB.currentText() == Action_Type.Time.name and 
        (value.isdigit() and 0 < int(value) < 21))):
            self.accept()
        else:
            QMessageBox.warning(self, "Alert", "Invalid value.")
            
