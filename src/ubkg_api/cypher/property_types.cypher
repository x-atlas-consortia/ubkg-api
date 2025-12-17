// December 2025
// Used by the /property-types endpoint

CALL db.propertyKeys()
YIELD propertyKey
RETURN apoc.coll.sort(COLLECT(propertyKey)) AS property_types
