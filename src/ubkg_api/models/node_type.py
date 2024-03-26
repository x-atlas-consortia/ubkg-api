# coding: utf-8

from __future__ import absolute_import

from . import util
from .base_model_ import Model

class NodeType(Model):

    """
    Model class representing a Node Type node.

    """

    def __init__(self,node_type=None):
        """
        :param node_type: a dictionary representing a set of node type nodes.

        """
        # Value Types
        self.openapi_types = {
            'node_type': list[dict]
        }
        # Attributes
        self.attribute_map = {
            'node_type': 'node_type'
        }
        # Property initialization.
        self._node_type = node_type

    def serialize(self):
        return {
            "node_type": self._node_type
        }

    @classmethod
    def from_dict(cls, dikt) -> 'NodeType':
        """Returns the dict as a model class.

        :param cls: A dict.
        :param dikt: A dict.
        :type: dict
        :return: The model class
        """
        return util.deserialize_model(dikt, cls)

    @property
    def node_type(self):
        """Gets the node_type of this NodeType.

        :return: The node_type of this NodeType.
        """
        return self._node_type

    @node_type.setter
    def node_type(self, node_type):
        """Sets the node_type of this NodeType.

        :param node_type: The semantic_types of this SemanticType.
        :type node_type: dict
        """

        self._node_type = node_type

