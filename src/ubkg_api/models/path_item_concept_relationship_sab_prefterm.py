# coding: utf-8

from __future__ import absolute_import

from . import util
from .base_model_ import Model


class PathItemConceptRelationshipSabPrefterm(Model):
    def __init__(self, path=None, item=None, concept=None, relationship=None, sab=None, prefterm=None):
        """PathItemConceptRelationshipSabPrefterm - a model defined in OpenAPI

        :param path: The path of this PathItemConceptRelationshipSabPrefterm.
        :type path: str
        :param item: The item of this PathItemConceptRelationshipSabPrefterm.
        :type item: str
        :param concept: The concept of this PathItemConceptRelationshipSabPrefterm.
        :type concept: str
        :param relationship: The relationship of this PathItemConceptRelationshipSabPrefterm.
        :type relationship: str
        :param sab: The sab of this PathItemConceptRelationshipSabPrefterm.
        :type sab: str
        :param prefterm: The prefterm of this PathItemConceptRelationshipSabPrefterm.
        :type prefterm: str
        """
        self.openapi_types = {
            'path': str,
            'item': str,
            'concept': str,
            'relationship': str,
            'sab': str,
            'prefterm': str
        }

        self.attribute_map = {
            'path': 'path',
            'item': 'item',
            'concept': 'concept',
            'relationship': 'relationship',
            'sab': 'sab',
            'prefterm': 'prefterm'
        }

        self._path = path
        self._item = item
        self._concept = concept
        self._relationship = relationship
        self._sab = sab
        self._prefterm = prefterm

    @classmethod
    def from_dict(cls, dikt) -> 'PathItemConceptRelationshipSabPrefterm':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PathItemConceptRelationshipSabPrefterm of this PathItemConceptRelationshipSabPrefterm.
        :rtype: PathItemConceptRelationshipSabPrefterm
        """
        return util.deserialize_model(dikt, cls)

    @property
    def path(self):
        """Gets the path of this PathItemConceptRelationshipSabPrefterm.


        :return: The path of this PathItemConceptRelationshipSabPrefterm.
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this PathItemConceptRelationshipSabPrefterm.


        :param path: The path of this PathItemConceptRelationshipSabPrefterm.
        :type path: str
        """

        self._path = path

    @property
    def item(self):
        """Gets the item of this PathItemConceptRelationshipSabPrefterm.


        :return: The item of this PathItemConceptRelationshipSabPrefterm.
        :rtype: str
        """
        return self._item

    @item.setter
    def item(self, item):
        """Sets the item of this PathItemConceptRelationshipSabPrefterm.


        :param item: The item of this PathItemConceptRelationshipSabPrefterm.
        :type item: str
        """

        self._item = item

    @property
    def concept(self):
        """Gets the concept of this PathItemConceptRelationshipSabPrefterm.


        :return: The concept of this PathItemConceptRelationshipSabPrefterm.
        :rtype: str
        """
        return self._concept

    @concept.setter
    def concept(self, concept):
        """Sets the concept of this PathItemConceptRelationshipSabPrefterm.


        :param concept: The concept of this PathItemConceptRelationshipSabPrefterm.
        :type concept: str
        """

        self._concept = concept

    @property
    def relationship(self):
        """Gets the relationship of this PathItemConceptRelationshipSabPrefterm.


        :return: The relationship of this PathItemConceptRelationshipSabPrefterm.
        :rtype: str
        """
        return self._relationship

    @relationship.setter
    def relationship(self, relationship):
        """Sets the relationship of this PathItemConceptRelationshipSabPrefterm.


        :param relationship: The relationship of this PathItemConceptRelationshipSabPrefterm.
        :type relationship: str
        """

        self._relationship = relationship

    @property
    def sab(self):
        """Gets the sab of this PathItemConceptRelationshipSabPrefterm.


        :return: The sab of this PathItemConceptRelationshipSabPrefterm.
        :rtype: str
        """
        return self._sab

    @sab.setter
    def sab(self, sab):
        """Sets the sab of this PathItemConceptRelationshipSabPrefterm.


        :param sab: The sab of this PathItemConceptRelationshipSabPrefterm.
        :type sab: str
        """

        self._sab = sab

    @property
    def prefterm(self):
        """Gets the prefterm of this PathItemConceptRelationshipSabPrefterm.


        :return: The prefterm of this PathItemConceptRelationshipSabPrefterm.
        :rtype: str
        """
        return self._prefterm

    @prefterm.setter
    def prefterm(self, prefterm):
        """Sets the prefterm of this PathItemConceptRelationshipSabPrefterm.


        :param prefterm: The prefterm of this PathItemConceptRelationshipSabPrefterm.
        :type prefterm: str
        """

        self._prefterm = prefterm

    def serialize(self):
        dict = {
            'path': self._path,
            'item': self._item,
            'concept': self._concept,
            'relationship': self._relationship,
            'sab': self._sab,
            'prefterm': self._prefterm
        }
        empty_keys = [k for k, v in dict.items() if v is None]
        for k in empty_keys:
            del dict[k]
        return dict
