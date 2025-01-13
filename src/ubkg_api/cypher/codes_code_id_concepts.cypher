// Used in the codes/{code_id}/concepts endpoint

// December 2024 - Changed to return only those concepts with a linked preferred term.

WITH $code_id AS query
MATCH (:Term)<-[d]-(a:Code)<-[:CODE]-(b:Concept)-[:PREF_TERM]->(c:Term)
WHERE ((a.CodeID = query) AND (b.CUI = d.CUI))
RETURN DISTINCT a.CodeID AS Code, b.CUI AS Concept, c.name as Prefterm
ORDER BY Code ASC, Concept