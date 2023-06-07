from __future__ import absolute_import

from .base_model_ import Model


class SabCodeTermRuiCode(Model):
    def __init__(self, sab=None, code=None, term=None, rui_code=None, organ_uberon=None):
        self._sab = sab
        self._code = code
        self._term = term
        self._rui_code = rui_code
        self._organ_uberon = organ_uberon

    def serialize(self):
        return {
            "sab": self._sab,
            "term": self._term,
            "code": self._code,
            "rui_code": self._rui_code,
            "organ_uberon": self._organ_uberon
        }