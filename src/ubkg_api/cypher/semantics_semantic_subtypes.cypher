// Called by the semantics/<semantic_id>/semantic_subtypes endpoint.
// The semantics_semantic_id_semantictypes_get_logic function in common_neo4j_logic.py will replace variables with
// leading dollar signs.

// Return the set of semantic types that are subtypes (have a relationship of
// ISA_STY with) the subtypes in $types identified by exact matches to of the following:
// 1. Name (e.g., "Anatomical Structure")
// 2. Type Unique Identifier (TUI) (e.g., "T017")

CALL
{
    MATCH (s:Semantic)-[:ISA_STY]->(q:Semantic)
    WHERE q.name IN [$types] OR q.TUI IN [$types]
    RETURN s
}
WITH s ORDER BY s.STN SKIP $skip LIMIT $limit
WITH DISTINCT {sty:s.name,tui:s.TUI,def:s.DEF,stn:s.STN}  AS stys
RETURN stys AS semantic_type