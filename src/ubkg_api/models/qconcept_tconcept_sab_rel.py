# coding: utf-8

from __future__ import absolute_import

from typing import List

from . import util
from .base_model_ import Model


class QconceptTconceptSabRel(Model):
    def __init__(self, query_concept_id=None, target_concept_id=None, sab=None, rel=None):
        """QconceptTconceptSabRel - a model defined in OpenAPI

        :param query_concept_id: The query_concept_id of this QconceptTconceptSabRel.
        :type query_concept_id: str
        :param target_concept_id: The target_concept_id of this QconceptTconceptSabRel.
        :type target_concept_id: str
        :param sab: The sab of this QconceptTconceptSabRel.
        :type sab: List[str]
        :param rel: The rel of this QconceptTconceptSabRel.
        :type rel: List[str]
        """
        self.openapi_types = {
            'query_concept_id': str,
            'target_concept_id': str,
            'sab': List[str],
            'rel': List[str]
        }

        self.attribute_map = {
            'query_concept_id': 'query_concept_id',
            'target_concept_id': 'target_concept_id',
            'sab': 'sab',
            'rel': 'rel'
        }

        self._query_concept_id = query_concept_id
        self._target_concept_id = target_concept_id
        self._sab = sab
        self._rel = rel

    @classmethod
    def from_dict(cls, dikt) -> 'QconceptTconceptSabRel':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The QconceptTconceptSabRel of this QconceptTconceptSabRel.
        :rtype: QconceptTconceptSabRel
        """
        return util.deserialize_model(dikt, cls)

    @property
    def query_concept_id(self):
        """Gets the query_concept_id of this QconceptTconceptSabRel.


        :return: The query_concept_id of this QconceptTconceptSabRel.
        :rtype: str
        """
        return self._query_concept_id

    @query_concept_id.setter
    def query_concept_id(self, query_concept_id):
        """Sets the query_concept_id of this QconceptTconceptSabRel.


        :param query_concept_id: The query_concept_id of this QconceptTconceptSabRel.
        :type query_concept_id: str
        """

        self._query_concept_id = query_concept_id

    @property
    def target_concept_id(self):
        """Gets the target_concept_id of this QconceptTconceptSabRel.


        :return: The target_concept_id of this QconceptTconceptSabRel.
        :rtype: str
        """
        return self._target_concept_id

    @target_concept_id.setter
    def target_concept_id(self, target_concept_id):
        """Sets the target_concept_id of this QconceptTconceptSabRel.


        :param target_concept_id: The target_concept_id of this QconceptTconceptSabRel.
        :type target_concept_id: str
        """

        self._target_concept_id = target_concept_id

    @property
    def sab(self):
        """Gets the sab of this QconceptTconceptSabRel.


        :return: The sab of this QconceptTconceptSabRel.
        :rtype: List[str]
        """
        return self._sab

    @sab.setter
    def sab(self, sab):
        """Sets the sab of this QconceptTconceptSabRel.


        :param sab: The sab of this QconceptTconceptSabRel.
        :type sab: List[str]
        """

        self._sab = sab

    @property
    def rel(self):
        """Gets the rel of this QconceptTconceptSabRel.


        :return: The rel of this QconceptTconceptSabRel.
        :rtype: List[str]
        """
        return self._rel

    @rel.setter
    def rel(self, rel):
        """Sets the rel of this QconceptTconceptSabRel.


        :param rel: The rel of this QconceptTconceptSabRel.
        :type rel: List[str]
        """

        self._rel = rel
