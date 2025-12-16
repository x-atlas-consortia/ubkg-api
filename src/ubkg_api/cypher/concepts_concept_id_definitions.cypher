// Used by the /concepts/{concept_id}/defintions endpoint.
// December 2025 - refactored as JSON streamed response

WITH [$concept_id] AS query
MATCH (a:Concept)-[:DEF]->(b:Definition)
  WHERE a.CUI in query
WITH COLLECT({sab:b.SAB, definition:b.DEF}) AS definitions
WITH definitions
UNWIND definitions AS definition
WITH definition
ORDER BY definition.definition
RETURN COLLECT(definition) AS definitions