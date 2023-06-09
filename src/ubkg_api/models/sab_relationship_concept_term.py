# coding: utf-8

from __future__ import absolute_import

from . import util
from .base_model_ import Model


class SabRelationshipConceptTerm(Model):
    def __init__(self, sab=None, relationship=None, concept=None, prefterm=None):
        """SabRelationshipConceptTerm - a model defined in OpenAPI

        :param sab: The sab of this SabRelationshipConceptTerm.
        :type sab: str
        :param relationship: The relationship of this SabRelationshipConceptTerm.
        :type relationship: str
        :param concept: The concept of this SabRelationshipConceptTerm.
        :type concept: str
        :param prefterm: The prefterm of this SabRelationshipConceptTerm.
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
    def from_dict(cls, dikt) -> 'SabRelationshipConceptTerm':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SabRelationshipConceptTerm of this SabRelationshipConceptTerm.
        :rtype: SabRelationshipConceptTerm
        """
        return util.deserialize_model(dikt, cls)

    @property
    def sab(self):
        """Gets the sab of this SabRelationshipConceptTerm.


        :return: The sab of this SabRelationshipConceptTerm.
        :rtype: str
        """
        return self._sab

    @sab.setter
    def sab(self, sab):
        """Sets the sab of this SabRelationshipConceptTerm.


        :param sab: The sab of this SabRelationshipConceptTerm.
        :type sab: str
        """

        self._sab = sab

    @property
    def relationship(self):
        """Gets the relationship of this SabRelationshipConceptTerm.


        :return: The relationship of this SabRelationshipConceptTerm.
        :rtype: str
        """
        return self._relationship

    @relationship.setter
    def relationship(self, relationship):
        """Sets the relationship of this SabRelationshipConceptTerm.


        :param relationship: The relationship of this SabRelationshipConceptTerm.
        :type relationship: str
        """

        self._relationship = relationship

    @property
    def concept(self):
        """Gets the concept of this SabRelationshipConceptTerm.


        :return: The concept of this SabRelationshipConceptTerm.
        :rtype: str
        """
        return self._concept

    @concept.setter
    def concept(self, concept):
        """Sets the concept of this SabRelationshipConceptTerm.


        :param concept: The concept of this SabRelationshipConceptTerm.
        :type concept: str
        """

        self._concept = concept

    @property
    def prefterm(self):
        """Gets the prefterm of this SabRelationshipConceptTerm.


        :return: The prefterm of this SabRelationshipConceptTerm.
        :rtype: str
        """
        return self._prefterm

    @prefterm.setter
    def prefterm(self, prefterm):
        """Sets the prefterm of this SabRelationshipConceptTerm.


        :param prefterm: The prefterm of this SabRelationshipConceptTerm.
        :type prefterm: str
        """

        self._prefterm = prefterm
