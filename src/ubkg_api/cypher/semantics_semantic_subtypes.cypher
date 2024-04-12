// Called by the semantics/<semantic_id>/semantic_subtypes endpoint.
// The semantics_semantic_id_semantictypes_get_logic function in common_neo4j_logic.py will replace variables with
// leading dollar signs.

// Return the set of semantic types that are subtypes (have a relationship of
// ISA_STY with) the subtypes in $types identified by exact matches to of the following:
// 1. Name (e.g., "Anatomical Structure")
// 2. Type Unique Identifier (TUI) (e.g., "T017")

// Optional filter on semantic type
WITH [$types] as type_query
WITH type_query
CALL
{
    WITH type_query
    MATCH (s:Semantic)-[:ISA_STY]->(q:Semantic)
    WHERE q.name IN type_query OR q.TUI IN type_query
    RETURN s
}
WITH type_query, s ORDER BY s.STN SKIP $skip LIMIT $limit
WITH COLLECT({sty:s.name,tui:s.TUI,def:s.DEF,stn:s.STN})  AS stys
RETURN stys AS semantic_subtype