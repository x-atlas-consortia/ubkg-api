# coding: utf-8

from __future__ import absolute_import

from . import util
from .base_model_ import Model
import neo4j

# property class
# from .concept_path_hop import ConceptPathHop
class ConceptGraph(Model):
    """
    Class representing a graph originating from a Concept node.

    """

    def __init__(self,graph=None):
        """
        :param graph: A dictionary that represents a graph originating from a Concept node.


        The dictionary conforms to the neo4j export format, and contains:
         - a nodes object, representing the nodes in the graph
         - a neo4j paths object, representing the paths originating from the Concept node
         - an edges object, representing the edges in the graph

        """
        # Value Types
        self.openapi_types = {
            'nodes': dict,
            'paths': dict,
            'edges': dict
        }
        # Attributes
        self.attribute_map = {
            'nodes': 'nodes',
            'paths': 'paths',
            'edges': 'edges'
        }
        # Property initialization
        self._nodes = graph['nodes']
        self._edges = graph['edges']

        # Translate neo4j paths object. Replicate the return for the "Table" view of the query returned for the
        # neo4j browser.

        listpath = []
        for path in graph['paths']:
            dictpath = {}

            #Start node
            dictpath['start'] = self.translate_node(path.start_node)

            #End node
            dictpath['end'] = self.translate_node(path.end_node)

            # Relationships
            dictpath['segments'] = self.translate_path(path)

            dictpath['length'] = float(len(path))

            listpath.append(dictpath)

        self._paths = listpath

    def translate_path(self, path=neo4j.graph.Path) -> list[dict]:
        """
        Translates a neo4j Path object into a dict that replicates the "segments" object in the browser.

        """
        listrel = []
        for rel in path.relationships:
            dictrel = {}

            # Start and end nodes for the relationship.
            dictrel['start'] = self.translate_node(rel.start_node)
            dictrel['end'] = self.translate_node(rel.end_node)

            # Relationship details
            dictrel_rel = {}
            dictrel_rel['identity'] = int(rel.element_id.split(':')[2])
            dictrel_rel['elementId'] = str(dictrel_rel['identity'])
            dictrel_rel['start'] = int(dictrel['start']['identity'])
            dictrel_rel['startNodeElementId'] = str(dictrel_rel['start'])
            dictrel_rel['end'] = int(dictrel['end']['identity'])
            dictrel_rel['endNodeElementId'] = str(dictrel_rel['end'])
            dictrel_rel['type'] = rel.type

            # Obtain relationship property information from rel.items, which is a collections.abc.ItemsView
            listproperties = []
            for i in rel.items():
                dictprop = {i[0]: i[1]}
                listproperties.append(dictprop)
            dictrel_rel['properties'] = listproperties

            dictrel['relationship'] = dictrel_rel

            listrel.append(dictrel)

        return listrel

    def translate_node(self, node=neo4j.graph.Node) -> dict:
        """
        Translates a neo4j node object into a dict that replicates a node object output in the browser.

        """

        dictret = {}
        identity = int(node.element_id.split(':')[2])

        # Extract labels from the node.labels Frozenset to list.
        listlabels = []
        for l in node.labels:
            listlabels.append(l)

        # Obtain property information from node.items, which is a collections.abc.ItemsView.
        listproperties=[]
        for i in node.items():
            # Extract key and value for property.
            dictprop = {i[0]:i[1]}
            listproperties.append(dictprop)

        return {'identity':identity,
                'labels':listlabels,
                'properties':listproperties,
                'elementId':str(identity)
            }


    def serialize(self):
        return {
            "nodes": self._nodes,
            "paths": self._paths,
            "edges": self._edges
        }

    @classmethod
    def from_dict(cls, dikt) -> 'ConceptGraph':
        """Returns the dict as a model class.

        :param cls: A dict.
        :param dikt: A dict.
        :type: dict
        :return: The model class
        :rtype: PathHop
        """
        return util.deserialize_model(dikt, cls)

    @property
    def nodes(self):
        """Gets the nodes of this ConceptGraph.

        :return: The nodes of this ConceptGraph.
        :rtype: nodes
        """
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        """Sets the graph of this ConceptGraph.

        :param nodes: The  nodes of this ConceptGraph.
        :type nodes: dict
        """

        self._nodes = nodes

    @property
    def paths(self):
        """Gets the paths of this ConceptGraph.

        :return: The paths of this ConceptGraph.
        :rtype: paths
        """
        return self._paths

    @paths.setter
    def paths(self, paths):
        """Sets the paths of this ConceptGraph.

        :param paths: The paths of this ConceptGraph.
        :type paths: dict
        """

        self._paths = paths

    @property
    def edges(self):
        """Gets the edges of this ConceptGraph.

        :return: The edges of this ConceptGraph.
        :rtype: edges
        """
        return self._edges

    @edges.setter
    def edges(self, edges):
        """Sets the edges of this ConceptGraph.

        :param edges: The edges of this ConceptGraph.
        :type edges: dict
        """

        self._edges = edges
