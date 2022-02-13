"""
User Inteface for inputting information for Action Widget
"""

from PyQt5.QtWidgets import QDialog, QMessageBox, QWidget
from src.interface.ui_action_widget import Ui_Dialog
from src.model.enums import ActionType
from utils import validHTMLTag


class ActionWidget(QDialog):
    """
    Action Widget Interface
    """

    def __init__(
        self,
        parent: QWidget,
        level_count: int,
        current_level: int,
        node_type: ActionType,
        value: str,
    ):
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
        self.interface.actionCB.setCurrentText(node_type.name.capitalize())
        self.interface.valueLE.setText(value)

        # Connecting function to button
        self.interface.buttonBox.accepted.connect(self.verify)
        self.interface.buttonBox.rejected.connect(self.reject)

    def run(self) -> dict:
        """
        Run the Action Widget interface
        """
        if self.exec_():
            #  If executed and validated successfully, then return user input
            node_attr: dict = {}
            node_attr["level"] = self.interface.levelCB.currentIndex()
            node_attr["action_type"] = ActionType[
                self.interface.actionCB.currentText().upper()
            ]
            node_attr["value"] = self.interface.valueLE.text()
            return node_attr
        self.show()
        return {}

    def verify(self) -> None:
        """
        Validates the user input
        """
        action_type: str = self.interface.actionCB.currentText().upper()
        value: str = self.interface.valueLE.text()

        # If user input is not an action type, then show error message
        if not hasattr(ActionType, action_type):
            QMessageBox.warning(self, "Alert", "Invalid Action option.")
            return None

        if ActionType[action_type] == ActionType.CLICK and validHTMLTag(value):
            # Accept if Action type is 'Click' and is valid HTML tag
            self.accept()
        elif ActionType[action_type] == ActionType.TIME and (
            value.isdigit() and 0 < int(value) < 21
        ):
            # Action type is 'Time' and in between 0 and 21, then accept
            self.accept()
        else:
            # If value is invalid, then show error message
            QMessageBox.warning(self, "Alert", "Invalid value.")
        return None
