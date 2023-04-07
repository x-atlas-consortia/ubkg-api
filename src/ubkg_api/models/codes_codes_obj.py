# coding: utf-8

from __future__ import absolute_import

from .base_model_ import Model
from . import util


class CodesCodesObj(Model):
    def __init__(self, concept=None, code=None, sab=None):
        """CodesCodesObj - a model defined in OpenAPI

        :param concept: The concept of this CodesCodesObj.
        :type concept: str
        :param code: The code of this CodesCodesObj.
        :type code: str
        :param sab: The sab of this CodesCodesObj.
        :type sab: str
        """
        self.openapi_types = {
            'concept': str,
            'code': str,
            'sab': str
        }

        self.attribute_map = {
            'concept': 'concept',
            'code': 'code',
            'sab': 'SAB'
        }

        self._concept = concept
        self._code = code
        self._sab = sab

    @classmethod
    def from_dict(cls, dikt) -> 'CodesCodesObj':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The CodesCodesObj of this CodesCodesObj.
        :rtype: CodesCodesObj
        """
        return util.deserialize_model(dikt, cls)

    @property
    def concept(self):
        """Gets the concept of this CodesCodesObj.


        :return: The concept of this CodesCodesObj.
        :rtype: str
        """
        return self._concept

    @concept.setter
    def concept(self, concept):
        """Sets the concept of this CodesCodesObj.


        :param concept: The concept of this CodesCodesObj.
        :type concept: str
        """

        self._concept = concept

    @property
    def code(self):
        """Gets the code of this CodesCodesObj.


        :return: The code of this CodesCodesObj.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this CodesCodesObj.


        :param code: The code of this CodesCodesObj.
        :type code: str
        """

        self._code = code

    @property
    def sab(self):
        """Gets the sab of this CodesCodesObj.


        :return: The sab of this CodesCodesObj.
        :rtype: str
        """
        return self._sab

    @sab.setter
    def sab(self, sab):
        """Sets the sab of this CodesCodesObj.


        :param sab: The sab of this CodesCodesObj.
        :type sab: str
        """

        self._sab = sab

    def serialize(self):
        return {
            "concept": self._concept,
            "code": self._code,
            "SAB": self._sab
        }
