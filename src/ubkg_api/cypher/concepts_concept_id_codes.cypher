// Used in the concepts/{concept_id}/codes endpoint

// The function that loads this query will replace concept_id and sab_filter with values
// from path and query parameters of the call to the endpoint.

WITH [$concept_id] AS query
MATCH (a:Concept)-[:CODE]->(b:Code)
  WHERE a.CUI IN query
  $sabfilter
RETURN b.CodeID AS codes

