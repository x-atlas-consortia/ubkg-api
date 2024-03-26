// Called by the semantics/<semantic_id>/semantic_types endpoint.
// The semantics_semantic_id_semantictypes_get_logic function in common_neo4j_logic.py will replace variables with
// leading dollar signs.

// Return either:
// 1. all semantic types
// 2. the set of semantic types in $types identified by exact matches to of the following:
//    a. Name (e.g., "Anatomical Structure")
//    b. Type Unique Identifier (TUI) (e.g., "T017")

CALL apoc.do.when(([$types] = []),
"MATCH (s:Semantic) RETURN s",
'MATCH (s:Semantic) WHERE s.name IN [$types] OR s.TUI IN [$types] RETURN s',
{})
YIELD value
WITH value.s as s ORDER BY s.STN SKIP $skip LIMIT $limit
WITH DISTINCT {sty:s.name,tui:s.TUI,def:s.DEF,stn:s.STN}  AS stys
RETURN stys AS semantic_type