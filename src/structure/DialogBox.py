"""
User Inteface for inputting information for Action Widget
"""

from structure import ActionNode, DataNode, InputNode


class DialogBox:
    @staticmethod
    def getAction(parent, levels, level=0, action="Click", value=""):
        actionNode = ActionNode(parent, levels, "Level " + str(level + 1), action, value)
        return actionNode.run()

    @staticmethod
    def getData(parent, levels, level=0, file_type="Text", value="", path="", all=0):
        dataNode = DataNode(parent, levels, "Level " + str(level + 1), file_type, value, path, all)
        return dataNode.run()

    @staticmethod
    def getInput(parent, levels, level=0, tag_type="Text/Combo Box", tag="", value=""):
        inputNode = InputNode(parent, levels, "Level " + str(level + 1), tag_type, tag, value)
        return inputNode.run()
