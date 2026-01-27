"""
Class that serializes neo4j Path objects as JSON.

Use case: the /concepts/paths endpoints of the ubkg-api.

"""
from neo4j.graph import Path, Node

class PathJSONSerializer(object):

    def __init__(self, graph=None):

        # graph is a list with elements 'edges', 'nodes', and 'paths'.

        self._nodes = graph[0]['nodes']
        self._edges = graph[0]['edges']

        # Serialize neo4j paths object.
        # Replicate the return for the "Table" view of the query returned for the
        # neo4j browser.

        listpath = []
        for path in graph[0]['paths']:
            dictpath = {'start': self._serialize_node(node=path.start_node),
                        'end': self._serialize_node(node=path.end_node),
                        'segments': self._serialize_path(path=path),
                        'length': float(len(path))}

            listpath.append(dictpath)

        self._paths = listpath

        self.json = {'nodes': self._nodes, 'edges': self._edges, 'paths': self._paths}

    def _serialize_node(self, node: Node) -> dict:

        """Serialize a Node object into a JSON-compatible dictionary.
        :param node: Node object
        """

        if not node:
            return {}
        return {
            "elementId": getattr(node, "element_id", None).split(':')[-1],  # Extract Node ID
            "identity": int(getattr(node, "element_id", None).split(':')[-1]),  # Extract Node ID
            "labels": list(node.labels) if hasattr(node, "labels") else [],
            "properties": [{key: node[key] for key in node.keys()}]  # Access properties using dictionary-like syntax
        }

    def _serialize_path(self, path: Path) -> list[dict]:
        """
        Translates a neo4j Path object into a dict that replicates the "segments" object in the browser.
        :param path: neo4j Path object
        """
        listrel = []
        for rel in path.relationships:
            dictrel = {}

            # Start and end nodes for the relationship.
            dictrel['start'] = self._serialize_node(rel.start_node)
            dictrel['end'] = self._serialize_node(rel.end_node)

            # Relationship details
            dictrel_rel = {'identity': int(rel.element_id.split(':')[2])}
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