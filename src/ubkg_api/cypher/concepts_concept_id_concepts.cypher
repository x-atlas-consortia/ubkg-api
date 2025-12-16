// Used by the /concepts/{concept_id}/concepts endpoint
// December 2025 - refactored to return JSON

WITH [$concept_id] AS query
MATCH (b:Concept)<-[c]-(d:Concept)
  WHERE b.CUI IN query
OPTIONAL MATCH (b)-[:PREF_TERM]->(a:Term)
OPTIONAL MATCH (d)-[:PREF_TERM]->(e:Term)
WITH COLLECT({sab:c.SAB, relationship:type(c), concept:d.CUI, prefterm:e.name}) AS concepts
WITH concepts
UNWIND concepts AS concept
WITH concept
ORDER BY concept.relationship, concept.concept, concept.prefterm
RETURN COLLECT(concept) AS concepts