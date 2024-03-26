# coding: utf-8

from __future__ import absolute_import

from . import util
from .base_model_ import Model

# property class
from .concept_path_hop import ConceptPathHop
class ConceptPath(Model):
    """
    Class representing a path between two Concept nodes.

    """

    def __init__(self,path_info=None):
        """
        :param pathinfo: A dictionary that represents a path between concepts.

        The dictionary contains
         - a list of dictionaries that correspond to the hops of the path, in order of occurrence in the path
         - the ordinal position of the path in the set of paths

        """
        # Value Types
        self.openapi_types = {
            'hops': list[ConceptPathHop],
            'position': int,
            'length': int
        }
        # Attributes
        self.attribute_map = {
            'hops': 'hops',
            'position': 'item',
            'length': 'length'
        }
        # Property initialization
        path = path_info.get('hops')

        pathhops = []
        for hop in path:
            sab = hop.get('SAB')
            source = hop.get('source')
            type = hop.get('type')
            target = hop.get('target')

            # Calculate the hop's position in the path.
            position = path.index(hop)+1

            pathhop = ConceptPathHop(sab=sab, source=source, type=type, target=target, hop=position)

            # Use the to_dict method of the Model base class to obtain a dictionary of the ConceptPathHop object.
            pathhopdict = pathhop.to_dict()
            pathhops.append(pathhopdict)

        self._hops = pathhops
        self._position = path_info.get('position')
        self._length = len(path)

    def serialize(self):
        return {
            "hops": self._hops,
            "length": self._length,
            "position": self._position
        }

    @classmethod
    def from_dict(cls, dikt) -> 'ConceptPath':
        """Returns the dict as a model class.

        :param cls: A dict.
        :param dikt: A dict.
        :type: dict
        :return: The model class
        :rtype: PathHop
        """
        return util.deserialize_model(dikt, cls)

    @property
    def hops(self):
        """Gets the hops of this ConceptPath.

        :return: The path of this ConceptPath.
        :rtype: PathHop
        """
        return self._hops

    @hops.setter
    def path(self, hops):
        """Sets the hops of this ConceptPath.

        :param hops: The hops of this ConceptPath.
        :type hops: str
        """

        self._hops = hops

    @property
    def length(self):
        """Gets the length of this ConceptPath.

        :return: The length of this ConceptPath.
        :rtype: int
        """
        return self._length

    @length.setter
    def length(self, length):
        """Sets the length of this ConceptPath.

        :param length: The path of this ConceptPath.
        :type length: str
        """

        self._length = length

    @property
    def position(self):
        """Gets the position of this ConceptPath.

        :return: The position of this ConceptPath.
        :rtype: int
        """
        return self._position

    @position.setter
    def position(self, position):
        """Sets the position of this ConceptPath.

        :param position: The position of this ConceptPath.
        :type position: str
        """

        self._position = position

