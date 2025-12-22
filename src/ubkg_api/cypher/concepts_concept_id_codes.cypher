// Used in the concepts/{concept_id}/codes endpoint

WITH [$concept_id] AS query
MATCH (a:Concept)-[:CODE]->(b:Code)
  WHERE a.CUI IN query
  $sabfilter
RETURN b.CodeID AS codes

