# coding: utf-8

from __future__ import absolute_import

from . import util
from .base_model_ import Model

class ConceptNode(Model):

    """
    Model class representing a "Concept node" object that translates and consolidates information from the
    subgraph that originates from a Concept node, involving Code, Term, Defintion, and Semantic Type nodes.

    """

    def __init__(self,node=None):
        """
        :param node: a dictionary representing a Concept node.

        """
        # Value Types
        self.openapi_types = {
            'node': list[dict]
        }
        # Attributes
        self.attribute_map = {
            'node': 'node'
        }
        # Property initialization.
        self._node = node


    def serialize(self):
        return {
            "node": self._node
        }

    @classmethod
    def from_dict(cls, dikt) -> 'ConceptNode':
        """Returns the dict as a model class.

        :param cls: A dict.
        :param dikt: A dict.
        :type: dict
        :return: The model class
        :rtype: PathHop
        """
        return util.deserialize_model(dikt, cls)

    @property
    def node(self):
        """Gets the node of this ConceptNode.

        :return: The node of this ConceptNode.
        """
        return self._node

    @node.setter
    def node(self, node):
        """Sets the concept of this ConceptNode.

        :param node: The concept of this ConceptNode.
        :type conceptNode: dict
        """

        self._node = node
