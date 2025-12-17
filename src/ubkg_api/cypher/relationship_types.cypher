// December 2025
// used by the /relationship-types endpoint.

CALL db.relationshipTypes()
YIELD relationshipType
RETURN apoc.coll.sort(COLLECT(relationshipType)) AS relationship_types
