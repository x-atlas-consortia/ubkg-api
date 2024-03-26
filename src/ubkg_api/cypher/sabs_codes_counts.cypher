// Used by /sabs/codes/counts
// The sab_code_count_get routine in common_neo4j_logic.py will replace the sab variable.

// Optional filter on SAB
WITH [$sab] as sab_query
WITH sab_query
// Get counts of codes by SAB.
CALL
{
    WITH sab_query
    OPTIONAL MATCH (n:Code) WHERE CASE WHEN sab_query=[] THEN 1=1 ELSE n.SAB in sab_query END
    RETURN n.SAB AS sab, COUNT(DISTINCT n) as code_count
    ORDER BY n.SAB
    SKIP $skip
    LIMIT $limit
}
WITH COLLECT({sab:sab, count:code_count}) AS sabs
RETURN sabs