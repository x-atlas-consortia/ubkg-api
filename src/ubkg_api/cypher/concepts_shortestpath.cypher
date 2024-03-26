//Used by the concepts/paths/shortestpath endpoint.

//The concepts_shortestpaths_logic function in common_neo4j_logic.py will replace variables preceded by the dollar sign.

// Identify the shortest path between the specified concept nodes, using the Dijkstra Algorithm with default weights.
CALL
{
MATCH (c:Concept {CUI: $origin_concept_id})
MATCH (d:Concept {CUI: $terminus_concept_id})
CALL apoc.algo.dijkstra(c, d, apoc.text.join([x IN [$rel] | "<"+x], "|"), "none", 1)
YIELD path
return path
}

// Filter to those paths that involve relationships with the specified values of SAB.
WITH path
WHERE ALL(r IN relationships(path) WHERE r.SAB IN [$sab])

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
WITH path_r
RETURN {hops:path_r} AS paths