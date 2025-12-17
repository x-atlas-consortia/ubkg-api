// December 2025
// used by the /terms/{id}/codes endpoint

WITH [$term_id] AS query
MATCH (a:Term)<-[b]-(c:Code)
  WHERE a.name IN query
WITH DISTINCT a.name AS Term, Type(b) AS TermType, c.CodeID AS Code
  ORDER BY Term, TermType, Code
RETURN {code:Code, termtype:TermType} AS codes