# coding: utf-8

from __future__ import absolute_import

from typing import List

from . import util
from .base_model_ import Model


class ConceptSabRel(Model):
    def __init__(self, query_concept_id=None, sab=None, rel=None):
        """ConceptSabRel - a model defined in OpenAPI

        :param query_concept_id: The query_concept_id of this ConceptSabRel.
        :type query_concept_id: str
        :param sab: The sab of this ConceptSabRel.
        :type sab: List[str]
        :param rel: The rel of this ConceptSabRel.
        :type rel: List[str]
        """
        self.openapi_types = {
            'query_concept_id': str,
            'sab': List[str],
            'rel': List[str]
        }

        self.attribute_map = {
            'query_concept_id': 'query_concept_id',
            'sab': 'sab',
            'rel': 'rel'
        }

        self._query_concept_id = query_concept_id
        self._sab = sab
        self._rel = rel

    @classmethod
    def from_dict(cls, dikt) -> 'ConceptSabRel':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ConceptSabRel of this ConceptSabRel.
        :rtype: ConceptSabRel
        """
        return util.deserialize_model(dikt, cls)

    @property
    def query_concept_id(self):
        """Gets the query_concept_id of this ConceptSabRel.


        :return: The query_concept_id of this ConceptSabRel.
        :rtype: str
        """
        return self._query_concept_id

    @query_concept_id.setter
    def query_concept_id(self, query_concept_id):
        """Sets the query_concept_id of this ConceptSabRel.


        :param query_concept_id: The query_concept_id of this ConceptSabRel.
        :type query_concept_id: str
        """

        self._query_concept_id = query_concept_id

    @property
    def sab(self):
        """Gets the sab of this ConceptSabRel.


        :return: The sab of this ConceptSabRel.
        :rtype: List[str]
        """
        return self._sab

    @sab.setter
    def sab(self, sab):
        """Sets the sab of this ConceptSabRel.


        :param sab: The sab of this ConceptSabRel.
        :type sab: List[str]
        """

        self._sab = sab

    @property
    def rel(self):
        """Gets the rel of this ConceptSabRel.


        :return: The rel of this ConceptSabRel.
        :rtype: List[str]
        """
        return self._rel

    @rel.setter
    def rel(self, rel):
        """Sets the rel of this ConceptSabRel.


        :param rel: The rel of this ConceptSabRel.
        :type rel: List[str]
        """

        self._rel = rel
