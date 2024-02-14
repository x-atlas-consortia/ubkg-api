// Used by the following endpoints:
// node_types/counts_by_sab/{node_type}

// Note that this query is capable of returning counts for all node types by sab; however, the execution time
// is likely to exceed API server timeouts for large databases such as the Data Distillery.

// Optional filter on label type
WITH [$node_type] as label_query
WITH label_query
// Either filter to specified labels or return information on all labels
CALL
{
    WITH label_query
    CALL db.labels() YIELD label WHERE (CASE WHEN label_query=[] THEN 1=1 ELSE label IN label_query END) RETURN label as match_label
}
// Optional filter on SAB
WITH match_label, [$sab] AS sab_query

// Return counts by label and sab
CALL
{
    WITH match_label,sab_query
    MATCH (n)
    WHERE match_label in labels(n)
    AND CASE WHEN sab_query=[] then 1=1 ELSE n.SAB in sab_query END
    RETURN COUNT(*) as label_count_by_sab, n.SAB as sab ORDER BY n.SAB
}
// Build output
WITH match_label,COLLECT({sab:sab, count:label_count_by_sab}) as label_sabs, SUM(label_count_by_sab) AS label_count
WITH COLLECT({label:match_label, count: label_count, sabs:label_sabs}) as node_types
RETURN {node_types:node_types} AS output