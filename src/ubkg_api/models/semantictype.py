# coding: utf-8

from __future__ import absolute_import

from . import util
from .base_model_ import Model

class SemanticType(Model):

    """
    Model class representing a Semantic Type node.

    """

    def __init__(self,semantic_type=None, position=None):
        """
        :param semantic_type: a dictionary representing a set of semantic type nodes.

        """
        # Value Types
        self.openapi_types = {
            'semantic_type': list[dict],
            'position': int
        }
        # Attributes
        self.attribute_map = {
            'semantic_type': 'semantic_type',
            'position': 'position'
        }
        # Property initialization.
        self._semantic_type = semantic_type
        if position is None:
            self._position = 0
        else:
            self._position = position

    def serialize(self):
        return {
            "semantic_type": self._semantic_type,
            "position": self._position
        }

    @classmethod
    def from_dict(cls, dikt) -> 'SemanticType':
        """Returns the dict as a model class.

        :param cls: A dict.
        :param dikt: A dict.
        :type: dict
        :return: The model class
        :rtype: PathHop
        """
        return util.deserialize_model(dikt, cls)

    @property
    def semantic_type(self):
        """Gets the semantic_type of this SemanticType.

        :return: The semantic_type of this SemanticType.
        """
        return self._semantic_type

    @semantic_type.setter
    def semantic_type(self, semantic_type):
        """Sets the hops of this SemanticType.

        :param semantic_type: The semantic_types of this SemanticType.
        :type semantic_types: dict
        """

        self._semantic_type = semantic_type

    @property
    def position(self):
        """Gets the position of this SemanticType.

        :return: The position of this SemanticType.
        """
        return self._position

    @position.setter
    def position(self, position):
        """Sets the hops of this position.

        :param position: The position of this SemanticType.
        :type position: int
        """

        self._position = position

