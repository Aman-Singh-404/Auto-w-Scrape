"""
Contains all enum entities
"""

from enum import Enum

NodeType = Enum("NodeType", "ACTION DATA INPUT")
ActionType = Enum("ActionType", "CLICK TIME")
DataType = Enum("DataType", "TEXT MEDIA TABLE")


class InputType(Enum):
    """
    Input Type Enum
    """

    TEXT = "Text/Combo Box"
    SELECT = "Radio Button/Check Box"

    @classmethod
    def hasValue(cls, value: str) -> bool:
        """
        Return true if value equals to enum value, else false
        """
        for input_type in InputType:
            if input_type.value == value:
                return True
        return False
