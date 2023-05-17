# coding: utf-8

from __future__ import absolute_import

from . import util
from .base_model_ import Model


class ConceptDetail(Model):
    def __init__(self, concept=None, prefterm=None):
        """ConceptDetail - a model defined in OpenAPI

        :param concept: The concept of this ConceptDetail.
        :type concept: str
        :param prefterm: The prefterm of this ConceptDetail.
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
        self._prefterm = prefterm

    @classmethod
    def from_dict(cls, dikt) -> 'ConceptDetail':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ConceptDetail of this ConceptDetail.
        :rtype: ConceptDetail
        """
        return util.deserialize_model(dikt, cls)

    @property
    def concept(self):
        """Gets the concept of this ConceptDetail.


        :return: The concept of this ConceptDetail.
        :rtype: str
        """
        return self._concept

    @concept.setter
    def concept(self, concept):
        """Sets the concept of this ConceptDetail.


        :param concept: The concept of this ConceptDetail.
        :type concept: str
        """

        self._concept = concept

    @property
    def prefterm(self):
        """Gets the prefterm of this ConceptDetail.


        :return: The prefterm of this ConceptDetail.
        :rtype: str
        """
        return self._prefterm

    @prefterm.setter
    def prefterm(self, prefterm):
        """Sets the prefterm of this ConceptDetail.


        :param prefterm: The prefterm of this ConceptDetail.
        :type prefterm: str
        """

        self._prefterm = prefterm

    def serialize(self):
        return {
            "concept": self._concept,
            "prefterm": self._prefterm
        }
