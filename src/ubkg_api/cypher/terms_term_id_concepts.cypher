// December 2025
// Used by the /terms/{id}/concepts endpoint.

WITH [$term_id] AS query
MATCH (a:Term)<-[b]-(c:Code)<-[:CODE]-(d:Concept)
        WHERE a.name IN query AND b.CUI = d.CUI
OPTIONAL MATCH (a:Term)<--(d:Concept) WHERE a.name IN query
RETURN DISTINCT a.name AS Term, d.CUI AS Concept
        ORDER BY Concept ASC