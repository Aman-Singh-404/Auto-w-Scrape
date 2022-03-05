"""
Node model for tree node
"""

from datetime import datetime
from enum import Enum
from src.model.enums import NodeType


class Node:
    """
    Node Model
    """

    def __init__(
        self, name: str, value: str, node_type: NodeType, level: int, inner_type: Enum
    ):
        # Intialise class variables
        self.name: str = name  # Store unique node name
        self.value: str = value  # Store content
        self.node_type: NodeType = node_type  # Indicate type of node
        self.level: int = level  # Store current level
        self.inner_type = inner_type  # Indicate method of respective node type
        self.order: datetime = datetime.now()  # Store current date for timestamping
        self.attributes: dict = {}  # Store additional node attributes

    def getAttribute(self, key: str) -> str:
        """
        Return value assciated with key in node attributes
        Raise exception with not exists
        """
        if not self.attributes.__contains__(key):
            raise Exception("Key doesn't exist")
        return self.attributes.get(key)

    def setAttribute(self, key: str, value: str) -> None:
        """
        Add/Update key-value pair in node attrbutes
        """
        self.attributes[key] = value
