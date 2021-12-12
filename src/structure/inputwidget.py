"""
User Inteface for inputting information for Input Widget
"""

from PyQt5.QtWidgets import QDialog, QMessageBox, QWidget
from src.interface.ui_input_widget import Ui_Dialog
from src.model.Enums import Input_Type
from utils import validHTMLTag


class InputWidget(QDialog):
    """
    Data Widget Interface
    """

    def __init__(self, parent: QWidget, level_count: int, current_level: int,
                 node_type: Input_Type, value: str, input_string: str):
        # Setup UI design
        QDialog.__init__(self, parent)
        self.interface = Ui_Dialog()
        self.interface.setupUi(self)
        self.setFixedSize(self.size())
        self.changeWindow(node_type.value)

        # Add number of levels from 1 to level_count
        for i in range(level_count):
            self.interface.levelCB.addItem(f"Level {i + 1}")

        # Setting atributes
        self.interface.levelCB.setCurrentIndex(current_level)
        self.interface.typeCB.setCurrentText(node_type.value)
        self.interface.valueLE.setText(value)
        self.interface.inputTE.setText(input_string)

        # Connecting function to button
        self.interface.typeCB.currentTextChanged.connect(self.changeWindow)
        self.interface.buttonBox.accepted.connect(self.verify)
        self.interface.buttonBox.rejected.connect(self.reject)

    def changeWindow(self, value) -> None:
        '''
        Change window layout on change of input type
        '''
        if value == Input_Type.Alphanumeric.value:
            self.interface.label_4.show()
            self.interface.inputTE.show()
            self.interface.buttonBox.move(179, 150)
            self.setFixedSize(350, 180)
        else:
            self.interface.label_4.hide()
            self.interface.inputTE.hide()
            self.interface.buttonBox.move(179, 100)
            self.setFixedSize(350, 130)

    def run(self) -> dict:
        '''
        Run the Input Widget interface
        '''
        if self.exec_():
            #  If executed and validated successfully, then return user input
            node_attr: dict = {}
            node_attr["level"] = self.interface.levelCB.currentIndex()
            node_attr["input_type"] = Input_Type[self.interface.typeCB.currentText()]
            node_attr["value"] = self.interface.valueLE.text()
            node_attr["input"] = self.interface.inputTE.text()
            return node_attr
        self.show()
        return {}

    def verify(self) -> None:
        '''
        Validates the user input
        '''
        input_type: str = self.interface.typeCB.currentText()
        value: str = self.interface.valueLE.text()
        input_string: str = self.interface.inputTE.toPlainText()

        if not Input_Type.hasValue(input_type):
            # If user input is not an data type, then show error message
            QMessageBox.warning(self, "Alert", "Invalid Input option.")
        elif not validHTMLTag(value):
            # If invalid HTML tag, show error
            QMessageBox.warning(self, "Alert", "HTML tag is invalid.")
        elif Input_Type.Alphanumeric.value == value and input_string == "":
            # If selected option is alpha-numeric and input value is empty, show error
            QMessageBox.warning(self, "Alert", "Input value is empty.")
        else:
            # If data type & value is valid, then accept
            self.accept()
