from enum import Enum

Node_Type = Enum("Node_Type", "Action Data Input")
Action_Type = Enum("Action_Type", "Click Time")
Data_Type = Enum("Action_Type", "Text Media Table")

class Input_Type(Enum):
    Alphanumeric = "Text/Combo Box"
    Select = "Radio Button/Check Box"

    def hasValue(value: str) -> bool:
        '''
        Return true if value equals to enum value, else false
        '''
        for input in Input_Type:
            if input.value == value: return True
        else:
            return False
