"""
User Inteface for inputting information for Data Widget
"""

from PyQt5.QtWidgets import QDialog, QMessageBox, QWidget
from src.interface.ui_data_widget import Ui_Dialog
from src.model.Enums import Data_Type
from utils import validHTMLTag


class DataWidget(QDialog):
    """
    Data Widget Interface
    """

    def __init__(self, parent: QWidget, level_count: int, current_level: int,
                 node_type: Data_Type, value: str):
        # Setup UI design
        QDialog.__init__(self, parent)
        self.interface = Ui_Dialog()
        self.interface.setupUi(self)
        self.setFixedSize(self.size())

        # Add number of levels from 1 to level_count
        for i in range(level_count):
            self.interface.levelCB.addItem(f"Level {i + 1}")

        # Setting atributes
        self.interface.levelCB.setCurrentIndex(current_level)
        self.interface.typeCB.setCurrentText(node_type.name)
        self.interface.valueLE.setText(value)

        # Connecting function to button
        self.interface.buttonBox.accepted.connect(self.verify)
        self.interface.buttonBox.rejected.connect(self.reject)

    def run(self) -> dict:
        '''
        Run the Data Widget interface
        '''
        if self.exec_():
            #  If executed and validated successfully, then return user input
            node_attr: dict = {}
            node_attr["level"] = self.interface.levelCB.currentIndex()
            node_attr["data_type"] = Data_Type[self.interface.typeCB.currentText()]
            node_attr["value"] = self.interface.valueLE.text()
            return node_attr
        self.show()
        return {}

    def verify(self) -> None:
        '''
        Validates the user input
        '''
        data_type: str = self.interface.typeCB.currentText()
        value: str = self.interface.valueLE.text()

        if not hasattr(Data_Type, data_type):
            # If user input is not an data type, then show error message
            QMessageBox.warning(self, "Alert", "Invalid Data option.")
        elif not validHTMLTag(value):
            # If invalid HTML tag, show error
            QMessageBox.warning(self, "Alert", "HTML tag is invalid.")
        else:
            # If data type & value is valid, then accept
            self.accept()
