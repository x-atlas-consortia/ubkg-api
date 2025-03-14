//Used by /sabs/codes/details/{sab}

// Note: this query would cause an OOME if all sabs were specified, so look only for one SAB.

// Required filter for SAB
WITH [$sab] as sab_query
WITH sab_query
// Get total code count
CALL
{
    WITH sab_query
    MATCH (n:Code) WHERE n.SAB IS NOT NULL AND n.SAB IN sab_query
    RETURN n.SAB as sab_match, COUNT(DISTINCT n) AS code_count
}
WITH sab_match,code_count
// Get code details
CALL
{
    WITH sab_match
    OPTIONAL MATCH (n:Code)
    WHERE n.SAB=sab_match
    RETURN DISTINCT n.CodeID AS code ORDER BY n.CodeID
}
// Get optional term details.
// March 2024 handles SABS like BIOMARKER with no terms for codes.
WITH sab_match,code_count,code
CALL
{
    WITH code
    OPTIONAL MATCH (p:Concept)-[:CODE]->(n:Code{CodeID:code})-[r]->(t:Term)
    WHERE r.CUI=p.CUI
    RETURN COLLECT(DISTINCT CASE WHEN t.name IS NULL THEN {} ELSE {term_type:TYPE(r),term:t.name} END) AS terms //ORDER BY n.CodeId
}
//Build output
WITH sab_match, code_count, code, terms
SKIP 0 LIMIT 1000
WITH sab_match, code_count,COLLECT({code:code,terms:terms}) AS codes
WITH {sab:sab_match, total_count:code_count,codes:codes} as sab
RETURN sab as output