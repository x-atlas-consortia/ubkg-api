// Used by the concepts/<identifier>/nodes endpoint.
// Returns representations of translated and consolidated information ("Concept nodes" or "concept subgraphs")
// for the Concepts that "match" a search term.

// A "Concept node" is the origin of a subgraph that links the Concept node to nodes of type Code, Term,
// Definition, and Semantic Type.
// A "match" is the union of the set of matches on text-based properties of nodes in the subgraph that originates from
// the Concept node.

// Identify the set of Concept nodes (actually, the subgraphs that originate from the Concept nodes) that match the search term.
// A search term can correspond to:
// 1. The preferred term for a Concept
// 2. The CUI for a Concept
// 3. A CodeID for a Code linked to a Concept (i.e., a Code node in the Concept node subgraph)
// 4. A term for a Code linked to a Concept (i.e., a Term node in the Concept node subgraph)


WITH [$search] AS query
CALL {

//1. Look for Concepts with preferred terms that match the search term.
WITH query
MATCH (n:Concept)-[:PREF_TERM]->(t:Term) WHERE t.name IN query
RETURN n

//2. Look for Concepts linked to Codes with terms that match the search term.
UNION
WITH query
MATCH (n:Concept)-[:CODE]->(:Code)-[tty]->(t:Term) WHERE tty.CUI = toString(n.CUI) AND t.name IN query
RETURN n

//3. Look for Concepts linked to Codes with CodeIDs that match the search term.
UNION
WITH query
MATCH (n:Concept)-[:CODE]->(c:Code) WHERE c.CodeID IN query
RETURN n

//4. Look for Concepts with CUIs that match the search term.
UNION
WITH query
MATCH (n:Concept) WHERE n.CUI IN query
RETURN n
}

// For each Concept node, obtain information from the subgraph.
WITH DISTINCT n
//SKIP 0 LIMIT 100

// 1. the preferred term for the Concept
OPTIONAL MATCH (n)-[:PREF_TERM]->(t:Term)
// 2. the set of Codes linked to the Concept
OPTIONAL MATCH (n)-[:CODE]->(code:Code)
// 3. the set of Term Types linked to the Codes for the Concept.
//    Note the filtering on CUI. This results in limiting to the codes that are the "primary cross-reference" codes for the concept.
OPTIONAL MATCH (n)-[:CODE]->(c:Code)-[tty]->(ct:Term) WHERE tty.CUI = toString(n.CUI)
// 4. the set of Definitions for the Concept
OPTIONAL MATCH (n)-[:DEF]->(d:Definition)
// 5. the set of Semantic Types for the Concept
OPTIONAL MATCH (n)-[:STY]->(s:Semantic)

// Build the conceptsubgraph object for each concept.

// 1. Collect "term objects" per code. A "term object" includes CUI of each term. The CUI of the terms of the primary cross-reference
// match the concept CUI.
WITH n, t, d, s, c, COLLECT(DISTINCT CASE WHEN ct.name IS NULL THEN NULL ELSE {name:ct.name, tty:Type(tty), ttyCUI:tty.CUI} END) AS termsPerCode

// 2. Build the codes array. Each member of the array has keys for codeid, sab, terms (without ttyCUI) and the computed primary flag.
WITH n, t, d, s,
COLLECT(DISTINCT CASE WHEN c.CodeID IS NULL THEN NULL ELSE
{
	codeid: c.CodeID,
	sab: c.SAB,
	terms: [tt IN termsPerCode WHERE tt IS NOT NULL | {name: tt.name, tty: tt.tty}]
} END) AS codes,


//3. Build the definitions array.
COLLECT (DISTINCT CASE WHEN d.DEF IS NULL THEN NULL ELSE {def: d.DEF, sab: d.SAB} END) AS defs,

//4. Build the semantic types array.
COLLECT (DISTINCT CASE WHEN s.name IS NULL THEN NULL ELSE {sty: s.name, tui: s.TUI, def: s.DEF, stn: s.STN} END) AS stys

// Build final conceptsubgraph object and set as a property of the concept node.

WITH n, {cui: n.CUI, pref_term: t.name, codes: codes, definitions: defs, semantic_types: stys} AS conceptsubgraph

// Ensure we handle a missing codes array safely
UNWIND coalesce(conceptsubgraph.codes, []) AS code

// Order by CUI, codeid
WITH n,conceptsubgraph, code
ORDER BY n.CUI, coalesce(code.codeid, '') ASC

// Re-collect codes in the desired order
WITH n, collect(code) AS orderedCodes, conceptsubgraph

// Rebuild the map with the ordered codes array
WITH {concept:{cui: conceptsubgraph.cui, pref_term: conceptsubgraph.pref_term, codes: orderedCodes, definitions: conceptsubgraph.definitions, semantic_types: conceptsubgraph.semantic_types}} AS conceptsubgraph
RETURN conceptsubgraph AS nodeobjects
