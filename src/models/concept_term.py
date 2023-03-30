# coding: utf-8

from __future__ import absolute_import

from . import util
from .base_model_ import Model


class ConceptTerm(Model):
    def __init__(self, concept=None, term=None):
        """ConceptTerm - a model defined in OpenAPI

        :param concept: The concept of this ConceptTerm.
        :type concept: str
        :param term: The term of this ConceptTerm.
        :type term: str
        """
        self.openapi_types = {
            'concept': str,
            'term': str
        }

        self.attribute_map = {
            'concept': 'concept',
            'term': 'term'
        }

        self._concept = concept
        self._term = term

    @classmethod
    def from_dict(cls, dikt) -> 'ConceptTerm':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ConceptTerm of this ConceptTerm.
        :rtype: ConceptTerm
        """
        return util.deserialize_model(dikt, cls)

    @property
    def concept(self):
        """Gets the concept of this ConceptTerm.


        :return: The concept of this ConceptTerm.
        :rtype: str
        """
        return self._concept

    @concept.setter
    def concept(self, concept):
        """Sets the concept of this ConceptTerm.


        :param concept: The concept of this ConceptTerm.
        :type concept: str
        """

        self._concept = concept

    @property
    def term(self):
        """Gets the term of this ConceptTerm.


        :return: The term of this ConceptTerm.
        :rtype: str
        """
        return self._term

    @term.setter
    def term(self, term):
        """Sets the term of this ConceptTerm.


        :param term: The term of this ConceptTerm.
        :type term: str
        """

        self._term = term

    def serialize(self):
        return {
            "concept": self._concept,
            "term": self._term
        }
