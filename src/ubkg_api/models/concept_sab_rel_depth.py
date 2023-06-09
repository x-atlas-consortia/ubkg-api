# coding: utf-8

from __future__ import absolute_import

from typing import List

from . import util
from .base_model_ import Model


class ConceptSabRelDepth(Model):
    def __init__(self, query_concept_id=None, sab=None, rel=None, depth=None):
        """ConceptSabRelDepth - a model defined in OpenAPI

        :param query_concept_id: The query_concept_id of this ConceptSabRelDepth.
        :type query_concept_id: str
        :param sab: The sab of this ConceptSabRelDepth.
        :type sab: List[str]
        :param rel: The rel of this ConceptSabRelDepth.
        :type rel: List[str]
        :param depth: The depth of this ConceptSabRelDepth.
        :type depth: int
        """
        self.openapi_types = {
            'query_concept_id': str,
            'sab': List[str],
            'rel': List[str],
            'depth': int
        }

        self.attribute_map = {
            'query_concept_id': 'query_concept_id',
            'sab': 'sab',
            'rel': 'rel',
            'depth': 'depth'
        }

        self._query_concept_id = query_concept_id
        self._sab = sab
        self._rel = rel
        self._depth = depth

    @classmethod
    def from_dict(cls, dikt) -> 'ConceptSabRelDepth':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ConceptSabRelDepth of this ConceptSabRelDepth.
        :rtype: ConceptSabRelDepth
        """
        return util.deserialize_model(dikt, cls)

    @property
    def query_concept_id(self):
        """Gets the query_concept_id of this ConceptSabRelDepth.


        :return: The query_concept_id of this ConceptSabRelDepth.
        :rtype: str
        """
        return self._query_concept_id

    @query_concept_id.setter
    def query_concept_id(self, query_concept_id):
        """Sets the query_concept_id of this ConceptSabRelDepth.


        :param query_concept_id: The query_concept_id of this ConceptSabRelDepth.
        :type query_concept_id: str
        """

        self._query_concept_id = query_concept_id

    @property
    def sab(self):
        """Gets the sab of this ConceptSabRelDepth.


        :return: The sab of this ConceptSabRelDepth.
        :rtype: List[str]
        """
        return self._sab

    @sab.setter
    def sab(self, sab):
        """Sets the sab of this ConceptSabRelDepth.


        :param sab: The sab of this ConceptSabRelDepth.
        :type sab: List[str]
        """

        self._sab = sab

    @property
    def rel(self):
        """Gets the rel of this ConceptSabRelDepth.


        :return: The rel of this ConceptSabRelDepth.
        :rtype: List[str]
        """
        return self._rel

    @rel.setter
    def rel(self, rel):
        """Sets the rel of this ConceptSabRelDepth.


        :param rel: The rel of this ConceptSabRelDepth.
        :type rel: List[str]
        """

        self._rel = rel

    @property
    def depth(self):
        """Gets the depth of this ConceptSabRelDepth.


        :return: The depth of this ConceptSabRelDepth.
        :rtype: int
        """
        return self._depth

    @depth.setter
    def depth(self, depth):
        """Sets the depth of this ConceptSabRelDepth.


        :param depth: The depth of this ConceptSabRelDepth.
        :type depth: int
        """

        self._depth = depth
