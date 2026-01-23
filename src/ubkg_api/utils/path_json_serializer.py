"""
Class that serializes neo4j Path objects as JSON.

Use case: the /concepts/paths endpoints of the ubkg-api.

"""
from neo4j.graph import Path, Node, Relationship

class PathJSONSerializer(object):

    def __init__(self, path: Path):

        self.path = path
        self.json = self._preprocess_resp(path)

    def _serialize_path(self, path: Path) -> dict:
        """Serialize a Neo4j Path object into a JSON-compatible dictionary."""

        # Extract all nodes in the path
        nodes = path.nodes if hasattr(path, "nodes") else []
        nodes_serialized = [self._serialize_node(node) for node in nodes]

        # Extract relationships in the path
        relationships = path.relationships if hasattr(path, "relationships") else []
        relationships_serialized = [self._serialize_relationship(rel) for rel in relationships]

        # Extract start and end nodes from the nodes list
        start_node = nodes_serialized[0] if nodes_serialized else {}
        end_node = nodes_serialized[-1] if nodes_serialized else {}

        return {
            "start": start_node,
            "end": end_node,
            "length": len(relationships),  # Length is the number of relationships
            "nodes": nodes_serialized,
            "relationships": relationships_serialized,
        }

    def _serialize_node(self, node: Node) -> dict:
        """Serialize a Node object into a JSON-compatible dictionary."""

        if not node:
            return {}
        return {
            "element_id": getattr(node, "element_id", None).split(':')[-1],  # Extract Node ID
            "identity": int(getattr(node, "element_id", None).split(':')[-1]),  # Extract Node ID
            "labels": list(node.labels) if hasattr(node, "labels") else [],
            "properties": [{key: node[key] for key in node.keys()}]  # Access properties using dictionary-like syntax
        }

    def _serialize_relationship(self, rel) -> dict:
        """Serialize a Relationship object into a JSON-compatible dictionary."""
        return {
            "type": getattr(rel, "type", None),
            "start_node": getattr(rel, "start_node", {}).get("element_id"),
            "end_node": getattr(rel, "end_node", {}).get("element_id"),
            #"properties": dict(rel) if hasattr(rel, "properties") else {}
            "properties": rel.properties if hasattr(rel, "properties") else {}
        }

    def _preprocess_resp(self, resp):

        """Traverse and preprocess the resp structure to serialize Path objects."""
        for graph_item in resp:

            # Process the "nodes" if present.
            if "nodes" in graph_item:
                graph_item["nodes"] = [
                    {   # Convert Node information if needed for further usage
                        "name": node.get("name"),
                        "id": node.get("id")
                    } for node in graph_item["nodes"]
                ]

            # Process the "paths" key, serialize every Path object
            if "paths" in graph_item:
                if isinstance(graph_item["paths"], list):
                    graph_item["paths"] = [
                        self._serialize_path(path) for path in graph_item["paths"]
                        if isinstance(path, Path)  # Verify that each element is a Path
                    ]

            # If additional keys like "edges" need processing, handle them here
            if "edges" in graph_item:
                # Ensure "edges" contains a list of dictionary-like objects
                if isinstance(graph_item["edges"], list):
                    graph_item["edges"] = [
                        {
                            "SAB": edge.get("SAB"),
                            "source": edge.get("source"),
                            "type": edge.get("type"),
                            "target": edge.get("target")
                        } for edge in graph_item["edges"]
                    ]

        return resp