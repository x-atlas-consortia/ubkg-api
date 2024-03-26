// Used by the following endpoints:
// /sabs/term_types
// /sabs/<sab>/term_types

// This query will result in a OOME error when looking for all SABs, so limit to the specified value.
WITH [$sab] as sab_query
WITH sab_query
CALL
{
    WITH sab_query
    OPTIONAL MATCH (c:Code)-[r]->() WHERE c.SAB in sab_query
    RETURN DISTINCT c.SAB AS sab_match, TYPE(r) AS term_type
    ORDER BY c.SAB
    SKIP $skip
    LIMIT $limit
}
WITH sab_match,COLLECT(term_type) AS term_types
WITH {sab:sab_match, term_types:term_types} AS sabs
RETURN sabs