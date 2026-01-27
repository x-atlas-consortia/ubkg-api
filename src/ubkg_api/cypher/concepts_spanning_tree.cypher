//Used by the concepts/paths/trees endpoint.

//The concepts_trees_get_logic function in common_neo4j_logic.py will replace variables preceded by the dollar sign.

// Identify the spanning tree starting from the specified node
// with path lengths in the specified range.
CALL
{
MATCH (c:Concept {CUI: $query_concept_id})
CALL apoc.path.spanningTree(c,{relationshipFilter:apoc.text.join([x IN [$rel] | "<"+x], "|"), labelFilter:"Concept", minLevel:$mindepth, maxLevel:$maxdepth})
YIELD path
return path
}

// Filter to those paths that involve relationships with the specified values of SAB.
WITH path
WHERE ALL(r IN relationships(path) WHERE r.SAB IN [$sab])

// Filter to a specified subset of paths--i.e., to support pagination.
// The result of the path.expand function is ordered in terms of Depth First Search, so the order of paths is invariant.
WITH path SKIP $skip LIMIT $limit

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
