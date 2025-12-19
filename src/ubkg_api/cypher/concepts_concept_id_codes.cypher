// Used in the concepts/{concept_id}/codes endpoint

WITH [$concept_id] AS query
MATCH (a:Concept)-[:CODE]->(b:Code)
  WHERE a.CUI IN query
  $sabfilter
WITH COLLECT(b.CodeID) AS codes
WITH codes
UNWIND codes AS code
WITH code
ORDER BY code
WITH COLLECT(code) AS codes
RETURN {codes:codes} AS codes