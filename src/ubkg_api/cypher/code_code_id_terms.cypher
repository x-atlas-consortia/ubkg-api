// Used in the codes/{code_id}/terms endpoint
// This query returns the list of Term nodes
// that link to the specified code.
// The list can be filtered to return only those terms of a particular "term type"--which, in the
// UBKG, corresponds to the type of relationship between the term and the code.

// The function that loads this query will replace values for code_id and termtype_filter.

CALL
{
    WITH $code_id AS query
    MATCH (p:Concept)-[:CODE]->(c:Code)-[r]->(t:Term)
    WHERE c.CodeID = query
    AND r.CUI = p.CUI
    $termtype_filter
    RETURN DISTINCT c.CodeID AS code, type(r) as term_type, t.name as term
}
WITH code, COLLECT(DISTINCT {term_type: term_type, term: term}) AS terms
RETURN {code:code,terms:terms} AS response