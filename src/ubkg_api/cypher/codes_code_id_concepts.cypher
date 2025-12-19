// Used in the codes/{code_id}/concepts endpoint

WITH $code_id AS query
MATCH (:Term)<-[d]-(a:Code)<-[:CODE]-(b:Concept)-[:PREF_TERM]->(c:Term)
// Note the link by CUI, which limits to those concepts with a linked preferred term.
WHERE ((a.CodeID = query) AND (b.CUI = d.CUI))
WITH COLLECT({concept:b.CUI,prefterm:c.name}) AS concepts
WITH concepts
UNWIND concepts AS concept
WITH concept
ORDER BY concept.concept
RETURN COLLECT(concept) AS concepts