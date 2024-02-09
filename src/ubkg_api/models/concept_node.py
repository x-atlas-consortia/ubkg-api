# coding: utf-8

from __future__ import absolute_import

from . import util
from .base_model_ import Model

class ConceptNode(Model):

    """
    Model class representing a fully-translated Concept node

    """

    def __init__(self,concept=None):
        """
        :param concept: a dictionary representing a set of semantic type nodes.

        """
        # Value Types
        self.openapi_types = {
            'concept': list[dict]
        }
        # Attributes
        self.attribute_map = {
            'concept': 'concept'
        }
        # Property initialization.
        self._concept = concept


    def serialize(self):
        return {
            "concept": self._concept
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
    def concept(self):
        """Gets the concept of this ConceptNode.

        :return: The concept of this ConceptNode.
        """
        return self._semantic_type

    @concept.setter
    def concept(self, concept):
        """Sets the concept of this ConceptNode.

        :param concept: The concept of this ConceptNode.
        :type conceptNode: dict
        """

        self._concept = concept
