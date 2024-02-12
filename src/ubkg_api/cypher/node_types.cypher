// Used by the following endpoints:
// node_types/counts
// node_types/counts/{node_type}

// Optional filter on label type
WITH [$node_type] as label_query
WITH label_query
// Either filter to specified labels or return information on all labels
CALL
{
    WITH label_query
    CALL db.labels() YIELD label WHERE (CASE WHEN label_query=[] THEN 1=1 ELSE label IN label_query END) RETURN label as match_label
}
WITH match_label

// Return counts by label
CALL
{
    WITH match_label
    OPTIONAL MATCH (n)
    WHERE match_label in labels(n)
    RETURN COUNT(*) as label_count
}
// Build output
WITH match_label,label_count
WITH COLLECT({label:match_label, count: label_count}) as node_types
RETURN {node_types:node_types} AS output