// Used in the codes/{code_id}/concepts endpoint

// The function that loads this query will replace code_id with a value
// from the path parameter of the call to the endpoint.

WITH $code_id AS query
MATCH (:Term)<-[d]-(a:Code)<-[:CODE]-(b:Concept)-[:PREF_TERM]->(c:Term)
// Note the link by CUI, which limits to those concepts with a linked preferred term.
WHERE ((a.CodeID = query) AND (b.CUI = d.CUI))
WITH COLLECT(DISTINCT {concept:b.CUI,prefterm:c.name}) AS concepts
WITH concepts
UNWIND concepts AS concept
WITH concept
ORDER BY concept.concept
RETURN COLLECT(concept) AS concepts