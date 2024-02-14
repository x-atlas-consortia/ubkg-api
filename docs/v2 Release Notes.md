# Unified Biomedical Knowledge Graph
## UBKG API Release Notes

## Version 2.0 (February 2024)

Version 2.0 is a significant refactoring and upgrade of the UBKG API.
### Support for neo4j version 5
The UBKG API has been upgraded to connect to and query UBKG instances hosted in version 5 of neo4j.
Endpoints (such as _/subgraphs_) also require relationship indexes, which were introduced in version 5.

### Configurable execution throttling
Some endpoints in the UBKG API feature parameters that can result in either long queries or large response payloads. 
This is especially the case for endpoints in _/concepts/paths_. The service host for the UBKG API may have constraints
on timeout or maximum payload size. 

The UBKG API now features settings that allow for graceful termination of endpoints  
before they result in server-initiated timeout or payload errors. The default settings are:
- maximum query run time (default: 28 seconds)
- maximum response payload size (default: 9 MB)

For endpoints with the potential for execution times that exceed the maximum, the UBKG API 
"timeboxes" the associated Cypher queries. Timeboxed queries terminate after a set time and 
return nothing, instead of continuing until timeout.

### neo4j Version compatibility checking
Endpoints in Version 2 of the UBKG API use features of neo4j that were introduced in version 5:
for example, the _/concepts/subgraphs_ endpoint searches on full text relationship indexes. 

The UBKG API compares the version of the UBKG instance with the minimal version required
for an endpoint, returning a HTTP 400 error message if the instance version is 
not compatible.

### Parameter validation and exception handling (HTTP 400 and 404 errors)
Version 2 of the UBKG API features extensive parameter validation, returning 
HTTP 400 messages with explanations. Examples of parameter validation include:
- checking for required parameter values
- checking for invalid parameter names
- confirming that parameters have values that are non-negative numbers
- confirming that the value of parameter that defines the mininum of a range (e.g., _mindepth_) is less than the value of the parameter that defines the maximum of the range (e.g., _maxdepth_)

When an endpoint returns no data, the UBKG API will raise a HTTP 404 exception and 
display a custom explanation. For endpoints with timeboxed queries, the custom 404 message will note the maximum query execution time.

If the size of an endpoint's response payload exceeds the maximum, the UBKG API will 
raise a HTTP 404 message, explaining the reason.

### POSTs are now GETs
All endpoints in Version 2 of the UBKG API use GET instead of POST.

### List parameter options
A number of endpoints feature parameters that can be lists: for example, the 
_rel_ parameter can be used to specify a set of relationship types with 
which to limit endpoint queries, such as {"isa", "part_of"}.

Version 2 of the UBKG API allows list parameters to be specified in two ways:
1. As a comma-delimited set of strings, optionally URL-encoded--e.g.,
   - rel=isa,part_of
   - rel=isa%3A%part_of
2. As a set of parameter-value pairs--e.g., 
   - rel=isa&rel=part_of

### Changes to endpoints
In addition to the aforementioned new features, version 2 of the 
UBKG API updates specific endpoints as follows:

#### Paths related endpoints
The following endpoints related to paths have been refactored:

| Old Endpoint            | New Endpoint                                                            | Purpose                                                                                          |
|-------------------------|-------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| _concepts/expand_       | _concepts/<concept_id>/paths/expand_                                    | Returns a set of paths originating from the specified Concept                                    |
| _concepts/trees_        | _concepts/<concept_id>/paths/trees_                                     | Return information on the Concepts in the spanning tree that originates from a specified Concept |
| _concepts/shorestpaths_ | _concepts/<origin_concept_id>/paths/shortestpath/<terminus_concept_id>_ | Return the shortest path between two Concepts, using Dykstra's algorithm with default weights    |

1. The format and content of the responses for these endpoints have been updated. Path-related endpoints 
return JSON arrays that represent a set of _paths_ in the UBKG. A path is an ordered set of objects representing _hops_ 
away from an originating concept node. Each hop in a path represents a 
relationship between two concept nodes. 
2. If a set of paths shares a common origin, the response includes an object representing
the originating node. 
3. For the case of the _concepts/shortestpath_ endpoint, the response includes objects representing both the
originating and terminal nodes.

Following is an example of a response that describes a path with one hop,
between CUI C0013227 (the _source_ of the hop) to CUI C2720507
(the _target_ of the hop), including the originating node (C2720507).

This response describes the relationship **(C0013227) - _isa_ -> (C2720507)**.
```
{
  "origin": {
    "concept": "C2720507",
    "prefterm": "SNOMED CT Concept (SNOMED RT+CTV3)"
  },
  "paths": [
    {
      "position": 1,
      "length": 1,
      "hops": [
        {
          "hop": 1,
          "sab": "SNOMEDCT_US",
          "source": {
            "concept": "C0013227",
            "prefterm": "Pharmaceutical Preparations"
          },
          "target": {
            "concept": "C2720507",
            "prefterm": "SNOMED CT Concept (SNOMED RT+CTV3)"
          },
          "type": "isa"
        }
      ]
    }
  ]
}
```

#### _/semantics/semantictypes_
The _/semantics/<term_id>/semantics_ endpoint has been updated to a pair of endpoints as described in the **New Endpoints** section.
The endpoint now allows searching by either semantic type name or Type Unique Identifier (TUI).


### New endpoints
The following endpoints were introduced in Version 2 of the UBKG API. Refer to the
SmartAPI documentation for details.

| Endpoint                                    | Purpose                                                                                                                                   |
|---------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| _/concepts/subgraph/_                       | Returns the set of pairs of concepts (i.e., one-hop paths) linked by a specified relationship type                                        |
| _/concepts/{identifier}/nodeobjects_        | Returns a set of "Concept Node objects" that "match" an identifier.  See _Concept Node objects_ below.                                    |
| _/database/server_                          | Returns basic information on the UBKG neo4j database                                                                                      |
| _/node_types_                               | Returns list of node types (node labels)                                                                                                  |
| _/node_types/counts_                        | See **Workaround for long-running queries**                                                                                               |
| _/node_types/{node_type}/counts_            | Returns counts of nodes in the database for a specified node type (label)                                                                 |
| _/node_types/counts_by_sab_                 | See **Workaround for long-running queries**                                                                                               |  
| _/node_types/{node_type}/counts_by_sab_     | Returns counts of nodes in the database for a specified node type (label), grouped by source (SAB)                                        |
| _/property_types_                           | Returns list of property types (keys)                                                                                                     |
| _/sabs/codes/counts_                        | Returns a set of sources (SABs), including counts of the codes associated with the sources                                                |
| _/sabs/{sab}/codes/counts/_                 | Returns the specified source (SAB), including the count of the codes associated with the source                                           |
| _/sabs/codes/details_                       | See **Workaround for long-running queries**                                                                                               |
| _/sabs/{sab}/codes/details_                 | Returns details on the codes associated with the specified source (SAB).                                                                  |    
| _/sabs/term_types_                          | See **Workaround for long-running queries**                                                                                               |
| _/sabs/{sab}/term_types_                    | Returns the list of term types (types of relationship) for relationships between the nodes that are defined by the specified source (SAB) |
| _/relationship_types_                       | Returns list of relationship types                                                                                                        |
| _/semantics/semantic_types_                 | Returns information on all Semantic Type nodes                                                                                            |
| _/semantics/semantic_types/{identifier}_    | Returns information on a specified Semantic Type                                                                                          |
| _/semantics/semantic_subtypes/{identifier}_ | Returns information on the set of Semantic Type nodes that are subtypes of the specified Semantic Type                                    |

##### Workaround for long-running queries
When executed against a large UBKG instance, the execution time of this endpoint will exceed either the server host timeout or server memory. 
This endpoint exists as a convenience; a custom 400 message will explain the issue and suggest alternatives.

See _Long-running endpoints_ under _**Known Limitations and Possible Enhancements**_ below.

##### Concept Node objects
A Concept node in the UBKG is the origin of a subgraph that links the 
Concept node to a set of Code, Term, Definition, and Semantic Type nodes. 
A _Concept Node object_ represents this subgraph as a set of Concept 
properties--i.e., all the Concept's linked Codes, terms, 
definitions, and semantic types. 

A "match" in the _/concepts/{identifier}/nodeobjects_ endpoint is an 
exact match between an identifier and a text-based property in a 
Concept Node object. Because an identifier may match properties in more than one Concept Node object, 
the endpoint can return multiple Concept Node objects.

Following is an example of the set a Concept Node objects related to the identifer "Cells":

```
{
    "nodeobjects": [
        {
            "node": {
                "codes": [
                    {
                        "codeid": "CARO:0000013",
                        "sab": "CARO",
                        "terms": [
                            {
                                "name": "cell",
                                "tty": "PT_CL"
                            }
                        ]
                    },
                    {
                        "codeid": "CL:0000000",
                        "sab": "CL",
                        "terms": [
                            {
                                "name": "cell",
                                "tty": "PT_PATO"
                            },
                            {
                                "name": "cell",
                                "tty": "PT_UBERON"
                            }
                        ]
                    },
                    {
                        "codeid": "LNC:LP18364-7",
                        "sab": "LNC",
                        "terms": [
                            {
                                "name": "Unspecified cells",
                                "tty": "LPN"
                            },
                            {
                                "name": "Unspecified cells",
                                "tty": "LPDN"
                            }
                        ]
                    },
                    {
                        "codeid": "FMA:68646",
                        "sab": "FMA",
                        "terms": [
                            {
                                "name": "Cell",
                                "tty": "PT"
                            },
                            {
                                "name": "Normal cell",
                                "tty": "SY"
                            },
                            {
                                "name": "Cellula",
                                "tty": "SY"
                            }
                        ]
                    },
                    {
                        "codeid": "PSY:08080",
                        "sab": "PSY",
                        "terms": [
                            {
                                "name": "Cells (Biology)",
                                "tty": "PT"
                            }
                        ]
                    },
                    {
                        "codeid": "CSP:0605-5409",
                        "sab": "CSP",
                        "terms": [
                            {
                                "name": "cell",
                                "tty": "PT"
                            }
                        ]
                    },
                    {
                        "codeid": "LNC:MTHU016342",
                        "sab": "LNC",
                        "terms": [
                            {
                                "name": "Unspecified cells",
                                "tty": "CN"
                            }
                        ]
                    },
                    {
                        "codeid": "MSH:D002477",
                        "sab": "MSH",
                        "terms": [
                            {
                                "name": "Cells",
                                "tty": "MH"
                            },
                            {
                                "name": "Cell",
                                "tty": "PM"
                            }
                        ]
                    },
                    {
                        "codeid": "LCH_NW:sh85021678",
                        "sab": "LCH_NW",
                        "terms": [
                            {
                                "name": "Cells",
                                "tty": "PT"
                            }
                        ]
                    },
                    {
                        "codeid": "FMA:71954",
                        "sab": "FMA",
                        "terms": [
                            {
                                "name": "Set of cells",
                                "tty": "PT"
                            },
                            {
                                "name": "Cells set",
                                "tty": "SY"
                            }
                        ]
                    },
                    {
                        "codeid": "UWDA:71954",
                        "sab": "UWDA",
                        "terms": [
                            {
                                "name": "Set of cells",
                                "tty": "PT"
                            }
                        ]
                    },
                    {
                        "codeid": "UWDA:68646",
                        "sab": "UWDA",
                        "terms": [
                            {
                                "name": "Cell",
                                "tty": "PT"
                            },
                            {
                                "name": "Cellula",
                                "tty": "SY"
                            }
                        ]
                    },
                    {
                        "codeid": "LNC:LP174115-8",
                        "sab": "LNC",
                        "terms": [
                            {
                                "name": "cells",
                                "tty": "LPDN"
                            },
                            {
                                "name": "cells",
                                "tty": "LPN"
                            }
                        ]
                    },
                    {
                        "codeid": "CHV:0000002603",
                        "sab": "CHV",
                        "terms": [
                            {
                                "name": "cell",
                                "tty": "PT"
                            },
                            {
                                "name": "cells",
                                "tty": "SY"
                            },
                            {
                                "name": "the cell",
                                "tty": "SY"
                            }
                        ]
                    },
                    {
                        "codeid": "LNC:LP14738-6",
                        "sab": "LNC",
                        "terms": [
                            {
                                "name": "Cells",
                                "tty": "LPDN"
                            },
                            {
                                "name": "Cells",
                                "tty": "LPN"
                            }
                        ]
                    },
                    {
                        "codeid": "CPM:10",
                        "sab": "CPM",
                        "terms": [
                            {
                                "name": "Cell",
                                "tty": "PT"
                            }
                        ]
                    },
                    {
                        "codeid": "LNC:MTHU001933",
                        "sab": "LNC",
                        "terms": [
                            {
                                "name": "Cells",
                                "tty": "CN"
                            }
                        ]
                    },
                    {
                        "codeid": "MTH:NOCODE",
                        "sab": "MTH",
                        "terms": [
                            {
                                "name": "Cells",
                                "tty": "SY"
                            },
                            {
                                "name": "Cells",
                                "tty": "PN"
                            }
                        ]
                    },
                    {
                        "codeid": "NCI:C12508",
                        "sab": "NCI",
                        "terms": [
                            {
                                "name": "Normal Cell",
                                "tty": "SY"
                            },
                            {
                                "name": "Cell Types",
                                "tty": "DN"
                            },
                            {
                                "name": "Cellular",
                                "tty": "AD"
                            },
                            {
                                "name": "Cells",
                                "tty": "SY"
                            },
                            {
                                "name": "Cell",
                                "tty": "PT"
                            },
                            {
                                "name": "Cell Type",
                                "tty": "SY"
                            }
                        ]
                    },
                    {
                        "codeid": "SNOMEDCT_US:4421005",
                        "sab": "SNOMEDCT_US",
                        "terms": [
                            {
                                "name": "Cellular structure",
                                "tty": "SY"
                            },
                            {
                                "name": "Cellular structures",
                                "tty": "SY"
                            },
                            {
                                "name": "Cell structure",
                                "tty": "PT"
                            },
                            {
                                "name": "Cell structure (cell structure)",
                                "tty": "FN"
                            },
                            {
                                "name": "Cell",
                                "tty": "SY"
                            }
                        ]
                    }
                ],
                "cui": "C0007634",
                "definitions": [
                    {
                        "def": "An anatomical structure that has as its parts a maximally connected cell compartment surrounded by a plasma membrane.",
                        "sab": "CARO"
                    },
                    {
                        "def": "A material entity of anatomical origin (part of or deriving from an organism) that has as its parts a maximally connected cell compartment surrounded by a plasma membrane.",
                        "sab": "CL"
                    },
                    {
                        "def": "The smallest units of living structure capable of independent existence, composed of a membrane-enclosed mass of protoplasm and containing a nucleus or nucleoid.",
                        "sab": "NCI"
                    },
                    {
                        "def": "OBSOLETE. The basic structural and functional unit of all organisms. Includes the plasma membrane and any external encapsulating structures such as the cell wall and cell envelope. [GOC:go_curators]",
                        "sab": "GO"
                    },
                    {
                        "def": "Anatomical structure that consists of cytoplasm surrounded by a plasma membrane, with or without the cell nucleus; together with other cells and intercellular matrix, it constitutes tissues. Examples: lymphocyte, fibroblast, erythrocyte, neuron.",
                        "sab": "UWDA"
                    },
                    {
                        "def": "Anatomical set which has as its direct members cells of same type or of different types.",
                        "sab": "FMA"
                    },
                    {
                        "def": "Anatomical structure, each instance of which has as its boundary the external surface of some maximally connected plasma membrane. Examples: lymphocyte, fibroblast, erythrocyte, neuron.",
                        "sab": "FMA"
                    },
                    {
                        "def": "minute protoplasmic masses that make up organized tissue, consisting of a nucleus which is surrounded by protoplasm which contains the various organelles and is enclosed in the cell or plasma membrane; cells are the fundamental, structural, and functional units of living organisms.",
                        "sab": "CSP"
                    },
                    {
                        "def": "The fundamental, structural, and functional units or subunits of living organisms. They are composed of CYTOPLASM containing various ORGANELLES and a CELL MEMBRANE boundary.",
                        "sab": "MSH"
                    }
                ],
                "pref_term": "Cells",
                "semantic_types": [
                    {
                        "def": "The fundamental structural and functional unit of living organisms.",
                        "stn": "A1.2.3.3",
                        "sty": "Cell",
                        "tui": "T025"
                    }
                ]
            }
        }
    ]
}
```

### Deprecated endpoints

The following endpoints were part of the initial release of the ubkg-api, 
but have been deprecated. Cypher queries and model class files for the deprecated endpoints are 
archived in folders named **deprecated** in the appropriate folders.

Endpoints can be returned to the UBKG API if an appropriate use case is identified.

| Endpoint                          | Reason for deprecating                                            |
|-----------------------------------|-------------------------------------------------------------------|
| _/concepts/<concept_id>/paths_    | Duplicates _/concepts/<concept_id>/paths/expand_                  |
| _/tui/{tui_id}/semantics_         | Functionality now part of _/semantic_types_ endpoints             |
| _/terms/{term_id}/concepts/terms_ | Functionality now part of _/concepts/<concept_id>/nodes_ endpoint |

# Known Limitations and Possible Enhancements

## Long-running endpoints
The current set of endpoints execute real-time Cypher queries. 
For very large UBKG instances (e.g., the Data Distillery), some endpoints
(especially those that calculate statistics such as counts) can result in errors of two types:
1. memory-related errors
2. timeout errors

Version 2 of the UBKG API does not execute queries with a known risk of failure; instead, 
related endpoints suggest workarounds using other endpoints.

### Examples
1. The query behind the _/sabs/codes/details_ will result in an Out of Memory Error (OOME) 
in the neo4j instance. The current workaround is to execute the version of the endpoint that accepts a specific SAB.
2. The query behind the _/node_type/counts_ will result in a query that is likely to exceed timeout. The current workaround is to execute the version of the endpont that accepts a specific node type. 

Because a UBKG instance is static, it would be more efficient to calculate relevant
statistics during generation in a summary analytical structure (e.g., summary
tables). The UBKG API would then be able to obtain statistical information 
about a UBKG instance by consulting the relevant summary data instead of attempting to 
calculate in real time.

## Other potential enhancements
### _/paths_ endpoints based on Code nodes instead of Concept nodes
Examples include _/expand_ for a Code node, or  _/shortest_path_ endpoint between two Code nodes.
The challenge is that there is a many:many relationship between Concept nodes and Code nodes. This requires
additional analysis.

### _/paths_ endpoints based on Semantic nodes
The challenge is that the subgraph of Semantic nodes appears to be cyclic.