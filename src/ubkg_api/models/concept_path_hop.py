# coding: utf-8

from __future__ import absolute_import

from . import util
from .base_model_ import Model
# property class
from .concept_prefterm import ConceptPrefterm

class ConceptPathHop(Model):
    """
    Class representing a single hop in a path involving Concept nodes. A hop is a triplet with a subject (source), object (target), and
    predicate (relationship).

    Example in JSON format
    {
        "hop": 1,
        "sab": "SNOMEDCT_US",
        "source": {
            "concept": "C0013227",
            "prefterm": "Pharmaceutical Preparations"
        },
        "target": {
            "concept": "C2720507",
            "prefterm": "SNOMED CT Concept (SNOMED RT+CTV3)
        }
        "type": "isa"
    }
    Describes the first hop in a path, from concept with CUI C0013227 to the concept with CUI C2720507,
    involving a 'isa' relationship defined in SAB SNOMEDCT_US.
    """

    def __init__(self, sab=None, source=None, type=None, target=None, hop=None):
        """
        :param sab: the SAB (source) that defines the predicate (relationship) of the hop in the path.
        :param source: the origin of the hop
        :param target: the end of the hop
        :param type: the type of predicate (relationship) for the hoop
        :param hop: the position of the hop in a path
        """

        # Value Types
        self.openapi_types = {
            'sab': str,
            'source': str,
            'type': str,
            'target': str,
            'hop': int
        }

        # Attributes
        self.attribute_map = {
            'sab': 'sab',
            'source': 'source',
            'type': 'type',
            'target': 'target',
            'hop': 'hop'
        }

        # Property initialization
        self._sab = sab

        source = ConceptPrefterm(concept=source.get('CUI'), prefterm=source.get('pref_term'))
        sourcedict = source.to_dict()
        self._source = sourcedict

        self._type = type
        target = ConceptPrefterm(concept=target.get('CUI'), prefterm=target.get('pref_term'))
        targetdict = target.to_dict()
        self._target = targetdict

        self._hop = hop

    def serialize(self):
        return {
            "sab": self._sab,
            "source": self._source,
            "type": self._type,
            "target": self._target,
            "hop": self._hop

        }

    @classmethod
    def from_dict(cls, dikt) -> 'ConceptPathHop':
        """Returns the dict as a model class.

        :param cls: A dict.
        :param dikt: A dict.
        :type: dict
        :return: The model class
        :rtype: ConceptPathHop
        """
        return util.deserialize_model(dikt, cls)

    @property
    def sab(self):
        """Gets the sab of this ConceptPathHop.

        :return: The sab of this ConceptPathHop.
        :rtype: str
        """
        return self._sab

    @sab.setter
    def sab(self, sab):
        """Sets the sab of this ConceptPathHop.

        :param sab: The sab of this ConceptPathHop.
        :type sab: str
        """

        self._sab = sab

    @property
    def source(self):
        """Gets the source of this ConceptPathHop.

        :return: The source of this ConceptPathHop.
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this ConceptPathHop.

        :param source: The source of this ConceptPathHop.
        :type source: str
        """

        self._source = source

    @property
    def type(self):
        """Gets the type of this ConceptPathHop.

        :return: The type of this ConceptPathHop.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ConceptPathHop.

        :param type: The type of this ConceptPathHop.
        :type type: str
        """

        self._type = type

    @property
    def target(self):
        """Gets the target of this ConceptPathHop.

        :return: The target of this ConceptPathHop.
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, target):
        """Sets the target of this ConceptPathHop.

        :param target: The target of this ConceptPathHop.
        :type target: str
        """

    @property
    def hop(self):
        """Gets the hop of this ConceptPathHop.

        :return: The hop of this ConceptPathHop.
        :rtype: str
        """
        return self._hop

    @hop.setter
    def hop(self, hop):
        """Sets the hop of this ConceptPathHop.

        :param hop: The hop of this ConceptPathHop.
        :type hop: int
        """

        self._hop = hop

