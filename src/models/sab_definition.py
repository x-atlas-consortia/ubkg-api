# coding: utf-8

from __future__ import absolute_import

from . import util
from .base_model_ import Model


class SabDefinition(Model):
    def __init__(self, sab=None, definition=None):
        """SabDefinition - a model defined in OpenAPI

        :param sab: The sab of this SabDefinition.
        :type sab: str
        :param definition: The definition of this SabDefinition.
        :type definition: str
        """
        self.openapi_types = {
            'sab': str,
            'definition': str
        }

        self.attribute_map = {
            'sab': 'sab',
            'definition': 'definition'
        }

        self._sab = sab
        self._definition = definition

    @classmethod
    def from_dict(cls, dikt) -> 'SabDefinition':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SabDefinition of this SabDefinition.
        :rtype: SabDefinition
        """
        return util.deserialize_model(dikt, cls)

    @property
    def sab(self):
        """Gets the sab of this SabDefinition.


        :return: The sab of this SabDefinition.
        :rtype: str
        """
        return self._sab

    @sab.setter
    def sab(self, sab):
        """Sets the sab of this SabDefinition.


        :param sab: The sab of this SabDefinition.
        :type sab: str
        """

        self._sab = sab

    @property
    def definition(self):
        """Gets the definition of this SabDefinition.


        :return: The definition of this SabDefinition.
        :rtype: str
        """
        return self._definition

    @definition.setter
    def definition(self, definition):
        """Sets the definition of this SabDefinition.


        :param definition: The definition of this SabDefinition.
        :type definition: str
        """

        self._definition = definition

    def serialize(self):
        return {
            "sab": self._sab,
            "definition": self._definition
        }