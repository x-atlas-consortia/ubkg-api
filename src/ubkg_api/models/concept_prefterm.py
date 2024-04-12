# coding: utf-8

from __future__ import absolute_import

from . import util
from .base_model_ import Model


class ConceptPrefterm(Model):
    def __init__(self, concept=None, prefterm=None):
        """ConceptPrefterm - a model defined in OpenAPI

        Represents a concept node in the UBKG.

        :param concept: The concept of this ConceptPrefterm.
        :type concept: str
        :param prefterm: The prefter  of this ConceptPrefterm.
        :type prefterm: str
        """
        self.openapi_types = {
            'concept': str,
            'prefterm': str
        }

        self.attribute_map = {
            'concept': 'concept',
            'prefterm': 'prefterm'
        }

        self._concept = concept
        self._prefterm  = prefterm

    def serialize(self):
        return {
            "concept": self._concept,
            "prefterm": self._prefterm
        }

    @classmethod
    def from_dict(cls, dikt) -> 'ConceptPrefterm':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ConceptPrefterm of this ConceptPrefterm.
        :rtype: ConceptPrefterm
        """
        return util.deserialize_model(dikt, cls)

    @property
    def concept(self):
        """Gets the concept of this ConceptPrefterm.


        :return: The concept of this ConceptPrefterm.
        :rtype: str
        """
        return self._concept

    @concept.setter
    def concept(self, concept):
        """Sets the concept of this ConceptPrefterm.


        :param concept: The concept of this ConceptPrefterm.
        :type concept: str
        """

        self._concept = concept

    @property
    def prefterm (self):
        """Gets the prefterm  of this ConceptPrefterm.


        :return: The prefterm  of this ConceptPrefterm.
        :rtype: str
        """
        return self._prefterm

    @prefterm .setter
    def prefterm(self, prefterm ):
        """Sets the prefter  of this ConceptPrefterm.


        :param prefterm : The prefterm of this ConceptPrefterm.
        :type prefterm : str
        """

        self._prefterm  = prefterm
