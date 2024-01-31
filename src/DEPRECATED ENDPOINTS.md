# Unified Biomedical Knowledge Graph
## UBKG API - Deprecated endpoints
The following endpoints were part of the initial release of the ubkg-api, 
but have been deprecated. 

Cypher queries and model class files for the deprecated endpoints are 
archived in folders named **deprecated** in the appropriate folders.

Endpoints can be returned to the UBKG API if an appropriate use case is identified.

# Endpoints

| Endpoint                           | Reason for deprecating                                         |
|------------------------------------|----------------------------------------------------------------|
| /concepts/{concept_id}/semantics   | Semantic types are a feature primarily of UMLS concepts.       |
| /semantics/{semantic_id}/semantics | Semantic types are a feature primarily of UMLS concepts.       |
| /tui/{tui_id}/semantics            | Type Unique Identifiers are a feature primarily of UMLS terms. |
| /terms/{term_id}/concepts/terms    | Incompatible with Cypher version 5                             |

