// Used by the concepts/<identifier>/nodes endpoint.
// Returns detailed information on Concepts that match a search term.

// Identify the Concept nodes that match the search parameter string.
// A search parameter string can correspond to:
// 1. The preferred term for a Concept
// 2. A term for a Code linked to a Concept
// 3. A CodeID for a Code linked to a Concept
// 4. The CUI for a Concept

WITH [$search] AS query
CALL {

//1. Look for Concepts with preferred terms that match the search parameter.
WITH query
MATCH (n:Concept)-[:PREF_TERM]->(t:Term) WHERE t.name IN query
RETURN n

//2. Look for Concepts linked to Codes with terms that match the search parameter.
UNION
WITH query
MATCH (n:Concept)-[:CODE]->(:Code)-[tty]->(t:Term) WHERE tty.CUI = toString(n.CUI) AND t.name IN query
RETURN n

//3. Look for Concepts linked to Codes with CodeIDs that match the search parameter.
UNION
WITH query
MATCH (n:Concept)-[:CODE]->(c:Code) WHERE c.CodeID IN query
RETURN n

//4. Look for Concepts with CUIs that match the search parameter.
UNION
WITH query
MATCH (n:Concept) WHERE n.CUI IN query
RETURN n
}

// For each Concept node, obtain:
WITH DISTINCT n
SKIP 0 LIMIT 100

// 1. the preferred term
OPTIONAL MATCH (n)-[:PREF_TERM]->(t:Term)
// 2. the set of Codes linked to the Concept
OPTIONAL MATCH (n)-[:CODE]->(code:Code)
// 3. the set of Term Types linked to the Codes for the Concept
OPTIONAL MATCH (n)-[:CODE]->(c:Code)-[tty]->(ct:Term) WHERE tty.CUI = toString(n.CUI)
// 4. the set of Definitions for the Concept
OPTIONAL MATCH (n)-[:DEF]->(d:Definition)
// 5. the set of Semantic Types for the Concept
OPTIONAL MATCH (n)-[:STY]->(s:Semantic)

// Compile return object
// 1. Create terms array - array of objects representing the terms for the Codes that link to Concepts.
WITH n,t,c,d,s,collect(DISTINCT{name:ct.name,tty:Type(tty)}) AS terms

// 2. Create array of objects representing Codes that link to Concepts. The codes object nests the terms array.
WITH n,t,collect(DISTINCT{codeid:c.CodeID,sab:c.SAB,terms:terms}) AS codes,

// 3. Create array of objects representing Definitions for the Concepts.
collect(DISTINCT{def:d.DEF,sab:d.SAB}) AS defs,

// 4. Create array of objects representing Semantic Types for the Concepts.
collect(DISTINCT{sty:s.name,tui:s.TUI,def:s.DEF,stn:s.STN}) AS stys

// Consolidate objects into an object of nested objects for the Concept. Each Concept object nests its corresponding
// arrays for Codes, Definitions, and Semantic Types.
WITH DISTINCT{cui:n.CUI,pref_term:t.name,codes:codes,definitions:defs,semantic_types:stys} AS concept
RETURN concept