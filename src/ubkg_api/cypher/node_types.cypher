// December 2025
// Used by the /node-types endpoint.
CALL db.labels()
YIELD label
RETURN apoc.coll.sort(COLLECT(label)) AS node_types
