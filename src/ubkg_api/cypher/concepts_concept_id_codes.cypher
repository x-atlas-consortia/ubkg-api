// Used in the concepts/{concept_id}/codes endpoint

WITH [$concept_id] AS query,
[$SAB] as sab
MATCH (a:Concept)-[:CODE]->(b:Code)
  WHERE a.CUI IN query
  AND (b.SAB IN sab OR sab = [])
WITH COLLECT(b.CodeID) AS codes
WITH codes
UNWIND codes AS code
WITH code
ORDER BY code
WITH COLLECT(code) AS codes
RETURN [{codes:codes}] AS codes