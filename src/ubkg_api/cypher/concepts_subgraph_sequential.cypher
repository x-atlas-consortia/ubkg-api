// Used by the concepts/paths/subgraph/sequential endpoint.
// Find all paths that start with Concept associated with the specified code and have relationships that are defined by specified SABs
// in the specified sequence.
// For example, the query will return all paths that start with the concept linked to UBERON:0004548 (left eye) and then have relationships:
// 1st level - "isa" relationship from UBERON
// 2nd level - "has_part" relationship from PATO

// SELECTION PARAMETERS
// Supplied by the calling function.
// 1. CUI corresponding to the starting concept of the expansion.
// If no CUI was supplied, query for all CUIs that have the first relationship.
WITH $startCUI AS initCUI,
// 2. Sequence of relationship types
//['isa','only_in_taxon','has_part'] as reltypes,
[$reltypes] AS reltypes,
// 3. Sequence of relationship SABs
//['CL','MP','EFO'] as relsabs,
[$relsabs] AS relsabs

// SELECTION OF STARTING CUIS
// Obtain either the CUI provided by the parameter OR the CUIs for all concepts that have the first relationship
// of the sequence.
CALL{
    WITH initCUI,reltypes, relsabs
    MATCH (cStart:Concept)-[rStart]->(c1:Concept)
    WHERE TYPE(rStart) = reltypes[0]
    AND rStart.SAB = relsabs[0]
    AND CASE WHEN initCUI <> "None" THEN cStart.CUI=initCUI ELSE 1=1 END
    RETURN DISTINCT cStart.CUI AS startCUI
    ORDER BY cStart.CUI
}

// FILTERING
// Two independent filters are required:
// 1. sequential relationship types (e.g., ["isa","has_part"])
// 2. sequential SAB properties (e.g. ["UBERON","PATO"])

// FIRST FILTER: sequence of relationship types.
// Expand from the starting concept, obtaining only those paths that exactly match the specified sequence of relationship types.
// Because the relationshipFilter specifies a sequence, relevant paths have length equal to the number of specified sequential relationships.
CALL
{
WITH startCUI,reltypes
MATCH (cStart:Concept {CUI:startCUI})
CALL apoc.path.expandConfig(cStart,
    {relationshipFilter:apoc.text.join([x IN reltypes | x], ">,"), beginSequenceAtStart: true,minLevel: 1, maxLevel: size(reltypes)})
YIELD path
return path
}
WITH path,reltypes,relsabs
WHERE length(path) = size(reltypes)

// SECOND FILTER: sequence of relationship SABs.
// Filter paths to those in which the SAB properties of relationships occur in the same order as the the specified sequence.
CALL
{
WITH path,relsabs
UNWIND(path) as path_check
UNWIND(relationships(path_check)) AS path_check_rels
RETURN COLLECT(path_check_rels.SAB) AS path_rel_sabs
}

WITH path,path_rel_sabs
WHERE path_rel_sabs=relsabs
WITH path
SKIP $skip LIMIT $limit
//For the filtered set of paths,

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
