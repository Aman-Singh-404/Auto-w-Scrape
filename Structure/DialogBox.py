from Structure.ActionNode import ActionNode
from Structure.DataNode import DataNode
from Structure.InputNode import InputNode


class DialogBox:
    def __init__(self, parent):
        self.parent = parent

    def getAction(self, levels, level=0, action="Click", value=""):
        actionNode = ActionNode(
            self.parent, levels, "Level " + str(level + 1), action, value
        )
        return actionNode.run()

    def getData(self, levels, level=0, file_type="Text", value="", path="", all=0):
        dataNode = DataNode(
            self.parent, levels, "Level " + str(level + 1), file_type, value, path, all
        )
        return dataNode.run()

    def getInput(self, levels, level=0, tag_type="Text/Combo Box", tag="", value=""):
        inputNode = InputNode(
            self.parent, levels, "Level " + str(level + 1), tag_type, tag, value
        )
        return inputNode.run()
