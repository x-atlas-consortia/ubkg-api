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

////////////////////////
// GRAPH FORMAT OPTION
// Returns a JSON in neo4j export format.

//For the set of paths,

// 1. Obtain an "edges" object with information on all relationships in all paths.
// 2. Obtain a "paths" object with path information on all paths.

UNWIND(relationships(path)) AS r
WITH path,collect({type:type(r),SAB:r.SAB,source:startNode(r).CUI,target:endNode(r).CUI}) AS path_r
WITH collect(path) as paths, apoc.coll.toSet(apoc.coll.flatten(COLLECT(path_r))) AS edges

// 3. Obtain a "nodes" object for all Concept nodes in all paths
UNWIND(paths) AS path
UNWIND(nodes(path)) AS n
// Obtain preferred terms for Concept nodes.
OPTIONAL MATCH (n)-[:PREF_TERM]->(t:Term)

WITH paths,edges,collect(DISTINCT{id:n.CUI,name:t.name}) AS nodes
RETURN {nodes:nodes, paths:paths, edges:edges} AS graph

////////////////////////
// ARRAY FORMAT OPTION - DEPRECATED
// Simplify the representation of a path to an array of JSON objects. Each object represents a single hop
// in the path, ordered by distance from the starting node.

// UNWIND(relationships(path)) AS r

// Obtain the preferred terms for the source and target concept nodes of every relationship.
// CALL
// {
  // WITH r
  // OPTIONAL MATCH (tStart:Term)<-[:PREF_TERM]-(pStart:Concept)-[r]->(pEnd:Concept)-[:PREF_TERM]->(tEnd:Term)
  // WHERE pStart.CUI=startNode(r).CUI AND pEnd.CUI=endNode(r).CUI
  // RETURN DISTINCT tStart, tEnd
// }

// Collect the ordered hops of each path into objects with properties for source node, end node, and relationships.
// WITH path,COLLECT(DISTINCT {type:type(r),SAB:r.SAB,source:{CUI:startNode(r).CUI,pref_term:tStart.name},target:{CUI:endNode(r).CUI,pref_term:tEnd.name}}) AS path_r
// WITH path_r
// RETURN {hops:path_r} AS paths