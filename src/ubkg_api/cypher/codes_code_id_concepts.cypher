// Used in the codes/{code_id}/concepts endpoint
// December 2025 - refactored to be JSON response
// December 2024 - Changed to return only those concepts with a linked preferred term.

WITH $code_id AS query
MATCH (:Term)<-[d]-(a:Code)<-[:CODE]-(b:Concept)-[:PREF_TERM]->(c:Term)
WHERE ((a.CodeID = query) AND (b.CUI = d.CUI))
WITH COLLECT({concept:b.CUI,prefterm:c.name}) AS concepts
WITH concepts
UNWIND concepts AS concept
WITH concept
ORDER BY concept.concept
RETURN COLLECT(concept) AS concepts