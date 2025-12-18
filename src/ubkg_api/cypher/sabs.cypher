// December 2025
// Used by the /sabs endpoint.

CALL
{
  MATCH (n:Code)
  RETURN DISTINCT n.SAB AS sab
  ORDER BY sab}
WITH COLLECT(sab) AS sabs
RETURN sabs
