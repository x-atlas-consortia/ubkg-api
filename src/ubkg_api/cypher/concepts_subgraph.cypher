//Used by the concepts/paths/subgraph endpoint.

//The concepts_subgraph_get_logic function in common_neo4j_logic.py will replace variables preceded by the dollar sign.

// Find all relationships of specified types defined by the specified set of SABs.
CALL
{
WITH apoc.text.join([x in [$sab] | x ], " OR ") AS sabs
CALL db.index.fulltext.queryRelationships("r_SAB",sabs)
YIELD relationship AS r WHERE TYPE(r) IN [$rel]
MATCH path=((n1)-[r]->(n2))
RETURN path
ORDER BY n1.CUI, n2.CUI
}

// Filter to a specified subset of paths--i.e., to support pagination.
WITH path SKIP $skip LIMIT $limit

// Simplify the representation of a path to an array of JSON objects. Each object represents a single hop
// in the path, ordered by distance from the starting node.

UNWIND(relationships(path)) AS r

// Obtain the preferred terms for the source and target concept nodes of every relationship.
CALL
{
  WITH r
  OPTIONAL MATCH (tStart:Term)<-[:PREF_TERM]-(pStart:Concept)-[r]->(pEnd:Concept)-[:PREF_TERM]->(tEnd:Term)
  WHERE pStart.CUI=startNode(r).CUI AND pEnd.CUI=endNode(r).CUI
  RETURN DISTINCT tStart, tEnd
}
// Collect the ordered hops of each path into objects with properties for source node, end node, and relationships.
WITH path,COLLECT(DISTINCT {type:type(r),SAB:r.SAB,source:{CUI:startNode(r).CUI,pref_term:tStart.name},target:{CUI:endNode(r).CUI,pref_term:tEnd.name}}) AS path_r
RETURN {hops:path_r} AS paths