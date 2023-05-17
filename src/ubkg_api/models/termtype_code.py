# coding: utf-8

from __future__ import absolute_import

from . import util
from .base_model_ import Model


class TermtypeCode(Model):
    def __init__(self, termtype=None, code=None):
        """TermtypeCode - a model defined in OpenAPI

        :param termtype: The termtype of this TermtypeCode.
        :type termtype: str
        :param code: The code of this TermtypeCode.
        :type code: str
        """
        self.openapi_types = {
            'termtype': str,
            'code': str
        }

        self.attribute_map = {
            'termtype': 'termtype',
            'code': 'code'
        }

        self._termtype = termtype
        self._code = code

    @classmethod
    def from_dict(cls, dikt) -> 'TermtypeCode':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The TermtypeCode of this TermtypeCode.
        :rtype: TermtypeCode
        """
        return util.deserialize_model(dikt, cls)

    @property
    def termtype(self):
        """Gets the termtype of this TermtypeCode.


        :return: The termtype of this TermtypeCode.
        :rtype: str
        """
        return self._termtype

    @termtype.setter
    def termtype(self, termtype):
        """Sets the termtype of this TermtypeCode.


        :param termtype: The termtype of this TermtypeCode.
        :type termtype: str
        """

        self._termtype = termtype

    @property
    def code(self):
        """Gets the code of this TermtypeCode.


        :return: The code of this TermtypeCode.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this TermtypeCode.


        :param code: The code of this TermtypeCode.
        :type code: str
        """

        self._code = code

    def serialize(self):
        return {
            "termtype": self._termtype,
            "code": self._code
        }
