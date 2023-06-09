# coding: utf-8

from __future__ import absolute_import

from . import util
from .base_model_ import Model


class QQST(Model):
    def __init__(self, query_tui=None, query_stn=None, semantic=None, tui=None, stn=None):
        """QQST - a model defined in OpenAPI

        :param query_tui: The query_tui of this QQST.
        :type query_tui: str
        :param query_stn: The query_stn of this QQST.
        :type query_stn: str
        :param semantic: The semantic of this QQST.
        :type semantic: str
        :param tui: The tui of this QQST.
        :type tui: str
        :param stn: The stn of this QQST.
        :type stn: str
        """
        self.openapi_types = {
            'query_tui': str,
            'query_stn': str,
            'semantic': str,
            'tui': str,
            'stn': str
        }

        self.attribute_map = {
            'query_tui': 'queryTUI',
            'query_stn': 'querySTN',
            'semantic': 'semantic',
            'tui': 'TUI',
            'stn': 'STN'
        }

        self._query_tui = query_tui
        self._query_stn = query_stn
        self._semantic = semantic
        self._tui = tui
        self._stn = stn

    @classmethod
    def from_dict(cls, dikt) -> 'QQST':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The QQST of this QQST.
        :rtype: QQST
        """
        return util.deserialize_model(dikt, cls)

    @property
    def query_tui(self):
        """Gets the query_tui of this QQST.


        :return: The query_tui of this QQST.
        :rtype: str
        """
        return self._query_tui

    @query_tui.setter
    def query_tui(self, query_tui):
        """Sets the query_tui of this QQST.


        :param query_tui: The query_tui of this QQST.
        :type query_tui: str
        """

        self._query_tui = query_tui

    @property
    def query_stn(self):
        """Gets the query_stn of this QQST.


        :return: The query_stn of this QQST.
        :rtype: str
        """
        return self._query_stn

    @query_stn.setter
    def query_stn(self, query_stn):
        """Sets the query_stn of this QQST.


        :param query_stn: The query_stn of this QQST.
        :type query_stn: str
        """

        self._query_stn = query_stn

    @property
    def semantic(self):
        """Gets the semantic of this QQST.


        :return: The semantic of this QQST.
        :rtype: str
        """
        return self._semantic

    @semantic.setter
    def semantic(self, semantic):
        """Sets the semantic of this QQST.


        :param semantic: The semantic of this QQST.
        :type semantic: str
        """

        self._semantic = semantic

    @property
    def tui(self):
        """Gets the tui of this QQST.


        :return: The tui of this QQST.
        :rtype: str
        """
        return self._tui

    @tui.setter
    def tui(self, tui):
        """Sets the tui of this QQST.


        :param tui: The tui of this QQST.
        :type tui: str
        """

        self._tui = tui

    @property
    def stn(self):
        """Gets the stn of this QQST.


        :return: The stn of this QQST.
        :rtype: str
        """
        return self._stn

    @stn.setter
    def stn(self, stn):
        """Sets the stn of this QQST.


        :param stn: The stn of this QQST.
        :type stn: str
        """

        self._stn = stn

    def serialize(self):
        return {
            "queryTUI": self._query_tui,
            "querySTN": self._query_stn,
            "semantic": self._semantic,
            "TUI": self._tui,
            "STN": self._stn
        }
