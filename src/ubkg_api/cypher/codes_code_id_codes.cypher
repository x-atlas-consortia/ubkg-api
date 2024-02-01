// Used in the codes/{code_id}/codes endpoint
// In general, a Concept node in UBKG is associated with Code nodes from multiple source vocabularies
// or ontologies (SABs). This query returns the list of Code nodes
// that share links to the same Concept node to which the specified code links.
// The list can be filtered to return only those codes from a particular SAB.

// The function that loads this query will replace values for code_id and sab_filter.

// Find the CUI for the concept to which the specified Code links.
CALL
{
    WITH $code_id AS query
    MATCH (a:Code)<-[:CODE]-(b:Concept)
    WHERE a.CodeID = query
    RETURN DISTINCT a.CodeID AS Code1, b.CUI as Concept
}

// Find all Codes that link to the Concept, including the original specified code.
// The separate OPTIONAL MATCH forces the response to include the original code that was specified.

WITH Code1, Concept
MATCH (b:Concept)-[:CODE]->(c:Code)
WHERE b.CUI=Concept
$sabfilter
RETURN Concept, c.CodeID AS Code2, c.SAB AS Sab2 ORDER BY Code1, Concept ASC, Code2, Sab2