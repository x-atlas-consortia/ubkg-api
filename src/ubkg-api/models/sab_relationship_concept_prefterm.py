# coding: utf-8

from __future__ import absolute_import

from dataclasses import dataclass

from . import util
from .base_model_ import Model


@dataclass
class SabRelationshipConceptPrefterm(Model):
    def __init__(self, sab=None, relationship=None, concept=None, prefterm=None):
        """SabRelationshipConceptPrefterm - a model defined in OpenAPI

        :param sab: The sab of this SabRelationshipConceptPrefterm.
        :type sab: str
        :param relationship: The relationship of this SabRelationshipConceptPrefterm.
        :type relationship: str
        :param concept: The concept of this SabRelationshipConceptPrefterm.
        :type concept: str
        :param prefterm: The prefterm of this SabRelationshipConceptPrefterm.
        :type prefterm: str
        """
        self.openapi_types = {
            'sab': str,
            'relationship': str,
            'concept': str,
            'prefterm': str
        }

        self.attribute_map = {
            'sab': 'sab',
            'relationship': 'relationship',
            'concept': 'concept',
            'prefterm': 'prefterm'
        }

        self._sab = sab
        self._relationship = relationship
        self._concept = concept
        self._prefterm = prefterm

    @classmethod
    def from_dict(cls, dikt) -> 'SabRelationshipConceptPrefterm':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SabRelationshipConceptPrefterm of this SabRelationshipConceptPrefterm.
        :rtype: SabRelationshipConceptPrefterm
        """
        return util.deserialize_model(dikt, cls)

    @property
    def sab(self):
        """Gets the sab of this SabRelationshipConceptPrefterm.


        :return: The sab of this SabRelationshipConceptPrefterm.
        :rtype: str
        """
        return self._sab

    @sab.setter
    def sab(self, sab):
        """Sets the sab of this SabRelationshipConceptPrefterm.


        :param sab: The sab of this SabRelationshipConceptPrefterm.
        :type sab: str
        """

        self._sab = sab

    @property
    def relationship(self):
        """Gets the relationship of this SabRelationshipConceptPrefterm.


        :return: The relationship of this SabRelationshipConceptPrefterm.
        :rtype: str
        """
        return self._relationship

    @relationship.setter
    def relationship(self, relationship):
        """Sets the relationship of this SabRelationshipConceptPrefterm.


        :param relationship: The relationship of this SabRelationshipConceptPrefterm.
        :type relationship: str
        """

        self._relationship = relationship

    @property
    def concept(self):
        """Gets the concept of this SabRelationshipConceptPrefterm.


        :return: The concept of this SabRelationshipConceptPrefterm.
        :rtype: str
        """
        return self._concept

    @concept.setter
    def concept(self, concept):
        """Sets the concept of this SabRelationshipConceptPrefterm.


        :param concept: The concept of this SabRelationshipConceptPrefterm.
        :type concept: str
        """

        self._concept = concept

    @property
    def prefterm(self):
        """Gets the prefterm of this SabRelationshipConceptPrefterm.


        :return: The prefterm of this SabRelationshipConceptPrefterm.
        :rtype: str
        """
        return self._prefterm

    @prefterm.setter
    def prefterm(self, prefterm):
        """Sets the prefterm of this SabRelationshipConceptPrefterm.


        :param prefterm: The prefterm of this SabRelationshipConceptPrefterm.
        :type prefterm: str
        """

        self._prefterm = prefterm

    def serialize(self):
        return {
            "sab": self._sab,
            "relationship": self._relationship,
            "concept": self._concept,
            "prefterm": self._prefterm
        }
