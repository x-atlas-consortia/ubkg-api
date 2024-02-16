# coding: utf-8

from __future__ import absolute_import

from src.ubkg_api.models import util
from src.ubkg_api.models.base_model_ import Model


class SemanticStn(Model):
    def __init__(self, semantic=None, stn=None):
        """SemanticStn - a model defined in OpenAPI

        :param semantic: The semantic of this SemanticStn.
        :type semantic: str
        :param stn: The stn of this SemanticStn.
        :type stn: str
        """
        self.openapi_types = {
            'semantic': str,
            'stn': str
        }

        self.attribute_map = {
            'semantic': 'semantic',
            'stn': 'STN'
        }

        self._semantic = semantic
        self._stn = stn

    @classmethod
    def from_dict(cls, dikt) -> 'SemanticStn':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SemanticStn of this SemanticStn.
        :rtype: SemanticStn
        """
        return util.deserialize_model(dikt, cls)

    @property
    def semantic(self):
        """Gets the semantic of this SemanticStn.


        :return: The semantic of this SemanticStn.
        :rtype: str
        """
        return self._semantic

    @semantic.setter
    def semantic(self, semantic):
        """Sets the semantic of this SemanticStn.


        :param semantic: The semantic of this SemanticStn.
        :type semantic: str
        """

        self._semantic = semantic

    @property
    def stn(self):
        """Gets the stn of this SemanticStn.


        :return: The stn of this SemanticStn.
        :rtype: str
        """
        return self._stn

    @stn.setter
    def stn(self, stn):
        """Sets the stn of this SemanticStn.


        :param stn: The stn of this SemanticStn.
        :type stn: str
        """

        self._stn = stn

    def serialize(self):
        return {
            "semantic": self._semantic,
            "STN": self._stn
        }
