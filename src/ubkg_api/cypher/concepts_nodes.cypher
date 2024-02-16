// Used by the concepts/<identifier>/nodes endpoint.
// Returns representations of translated and consolidated information ("Concept nodes")
// for the Concepts that "match" a search term.
// A "Concept node" is the origin of a subgraph that links the Concept node to nodes of type Code, Term,
// Definition, and Semantic Type.
// A "match" is the union of the set of matches on text-based properties of nodes in the subgraph that originates from
// the Concept node.

// Identify the Concept nodes (actually, the subgraphs that originate from the Concept nodes) that match the search term.
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
SKIP 0 LIMIT 100

// 1. the preferred term for the Concept
OPTIONAL MATCH (n)-[:PREF_TERM]->(t:Term)
// 2. the set of Codes linked to the Concept
OPTIONAL MATCH (n)-[:CODE]->(code:Code)
// 3. the set of Term Types linked to the Codes for the Concept
OPTIONAL MATCH (n)-[:CODE]->(c:Code)-[tty]->(ct:Term) WHERE tty.CUI = toString(n.CUI)
// 4. the set of Definitions for the Concept
OPTIONAL MATCH (n)-[:DEF]->(d:Definition)
// 5. the set of Semantic Types for the Concept
OPTIONAL MATCH (n)-[:STY]->(s:Semantic)

// Build the "Concept node" object.

// 1. Create Terms object - array of objects representing the Term nodes for the Code nodes that link to Concept nodes.
WITH n,t,c,d,s,collect(DISTINCT{name:ct.name,tty:Type(tty)}) AS terms

// 2. Create Codes object - array of objects representing Code nodes that link to Concept nodes.
//    The Terms object will be a key of the Codes object.
WITH n,t,collect(DISTINCT{codeid:c.CodeID,sab:c.SAB,terms:terms}) AS codes,

// 3. Create Definitions object - array of objects representing Definition nodes that link to Concept nodes.
collect(DISTINCT{def:d.DEF,sab:d.SAB}) AS defs,

// 4. Create Semantic Types object - array of objects representing Semantic Type nodes that link to Concepts nodes.
collect(DISTINCT{sty:s.name,tui:s.TUI,def:s.DEF,stn:s.STN}) AS stys

// Consolidate Codes, Definitions, and Semantic Types objects into an node object representing the Concept subgraph.
WITH DISTINCT{cui:n.CUI,pref_term:t.name,codes:codes,definitions:defs,semantic_types:stys} AS nodeobject
RETURN nodeobject