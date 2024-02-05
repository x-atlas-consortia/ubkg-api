# coding: utf-8

from __future__ import absolute_import

from . import util
from .base_model_ import Model

# subclass
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
            'path': list[ConceptPathHop],
            'item': int,
            'length': int
        }
        # Attributes
        self.attribute_map = {
            'path': 'path',
            'item': 'item',
            'length': 'length'
        }
        # Property initialization
        path = path_info.get('path')

        pathhops = []
        for hop in path:
            sab = hop.get('SAB')
            source = hop.get('source')
            type = hop.get('type')
            target = hop.get('target')

            # Calculate the hop's position in the path.
            hop_index = path.index(hop)+1

            pathhop = ConceptPathHop(sab=sab, source=source, type=type, target=target, hop=hop_index)

            # Use the to_dict method of the Model base class to obtain a dictionary of the ConceptPathHop object.
            pathhopdict = pathhop.to_dict()
            pathhops.append(pathhopdict)

        self._path = pathhops
        self._item = path_info.get('item')
        self._length = len(path)

    def serialize(self):
        return {
            "path": self._path,
            "length": self._length,
            "item": self._item
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
    def path(self):
        """Gets the path of this ConceptPath.

        :return: The path of this ConceptPath.
        :rtype: PathHop
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this ConceptPath.

        :param path: The path of this ConceptPath.
        :type path: str
        """

        self._path = path

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
    def item(self):
        """Gets the item of this ConceptPath.

        :return: The item of this ConceptPath.
        :rtype: int
        """
        return self._item

    @item.setter
    def item(self, item):
        """Sets the item of this ConceptPath.

        :param item: The item of this ConceptPath.
        :type item: str
        """

        self._item = item

