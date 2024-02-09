// Called by the /semantics/<semantic_id>/semantictypes
// The semantics_semantic_id_semantictypes_get_logic function in common_neo4j_logic.py will replace variables with
// leading dollar signs.

// If a list of values is provided, return the set of semantic types that are subtypes (have a relationship of
// ISA_STY with) the subtypes identified by exact matches to of the following:
// 1. Name (e.g., "Anatomical Structure")
// 2. Type Unique Identifier (TUI) (e.g., "T017")
// Otherwise, return all semantic types.

WITH [$types] AS query
CALL apoc.do.when((query = []),
"MATCH (s:Semantic) RETURN s",
"MATCH (s:Semantic)-[:ISA_STY]->(q:Semantic) WHERE q.name IN "+apoc.text.toCypher(query)+" OR q.TUI IN "+apoc.text.toCypher(query)+" RETURN s",
{})
YIELD value
WITH value.s as s ORDER BY s.STN SKIP $skip LIMIT $limit
WITH DISTINCT {sty:s.name,tui:s.TUI,def:s.DEF,stn:s.STN}  AS stys
RETURN stys AS semantic_type