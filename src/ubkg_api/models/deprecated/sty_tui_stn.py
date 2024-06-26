# coding: utf-8

from __future__ import absolute_import

from src.ubkg_api.models import util
from src.ubkg_api.models.base_model_ import Model


class StyTuiStn(Model):
    def __init__(self, sty=None, tui=None, stn=None):
        """StyTuiStn - a model defined in OpenAPI

        :param sty: The sty of this StyTuiStn.
        :type sty: str
        :param tui: The tui of this StyTuiStn.
        :type tui: str
        :param stn: The stn of this StyTuiStn.
        :type stn: str
        """
        self.openapi_types = {
            'sty': str,
            'tui': str,
            'stn': str
        }

        self.attribute_map = {
            'sty': 'sty',
            'tui': 'tui',
            'stn': 'stn'
        }

        self._sty = sty
        self._tui = tui
        self._stn = stn

    @classmethod
    def from_dict(cls, dikt) -> 'StyTuiStn':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The StyTuiStn of this StyTuiStn.
        :rtype: StyTuiStn
        """
        return util.deserialize_model(dikt, cls)

    @property
    def sty(self):
        """Gets the sty of this StyTuiStn.


        :return: The sty of this StyTuiStn.
        :rtype: str
        """
        return self._sty

    @sty.setter
    def sty(self, sty):
        """Sets the sty of this StyTuiStn.


        :param sty: The sty of this StyTuiStn.
        :type sty: str
        """

        self._sty = sty

    @property
    def tui(self):
        """Gets the tui of this StyTuiStn.


        :return: The tui of this StyTuiStn.
        :rtype: str
        """
        return self._tui

    @tui.setter
    def tui(self, tui):
        """Sets the tui of this StyTuiStn.


        :param tui: The tui of this StyTuiStn.
        :type tui: str
        """

        self._tui = tui

    @property
    def stn(self):
        """Gets the stn of this StyTuiStn.


        :return: The stn of this StyTuiStn.
        :rtype: str
        """
        return self._stn

    @stn.setter
    def stn(self, stn):
        """Sets the stn of this StyTuiStn.


        :param stn: The stn of this StyTuiStn.
        :type stn: str
        """

        self._stn = stn

    def serialize(self):
        return {
            "sty": self._sty,
            "tui": self._tui,
            "stn": self._stn
        }
