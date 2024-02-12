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
before they result in server-initiated timeout or payload errors. The settings are:
- maximum query run time (default: 28 seconds)
- maximum response payload size (default: 9 MB)

For endpoints with the potential for execution times that exceed the maximum, the UBKG API 
"timeboxes" the associated Cypher queries. Timeboxed queries terminate after a set time and 
return nothing, instead of continuing until timeout

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
1. The following endpoints related to paths have been moved from the _concepts/<concept-id>/_ URL base to 
the _concepts/<concept_id>/paths/_ URL path:
   - _concepts/<concept_id>/paths/expand
   - _concepts/<concept_id>/paths/trees
   - _concepts/<concept_id>/paths/shortestpath
2. The _../shortestpaths_ endpoint was renamed _../shortestpath_.
3. The format and content of the responses for these endpoints have been updated. Path-related endpoints 
return JSON arrays that represent a set of _paths_ in the UBKG. A path is an ordered set of objects representing _hops_ 
away from an originating concept node. Each hop in a path represents a 
relationship between two concept nodes. 
4. A new endpoint (_concepts/subgraphs_) returns a _subgraph_ of the UBKG--i.e. the set of pairs of concept nodes (or one-hop paths) linked by a specified relationship type. 
5. If a set of paths shares a common origin, the response includes an object representing
the originating node. 
6. For the case of the _concepts/shortestpath_ endpoint, the response includes an object representing the
terminal node.

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


#### New endpoints
The following endpoints were introduced in Version 2 of the UBKG API. Refer to the
SmartAPI documentation for details.

| Endpoint                                    | Purpose                                                                                                  |
|---------------------------------------------|----------------------------------------------------------------------------------------------------------|
| _/concepts/subgraph/_                       | Returns the set of pairs of concepts (i.e., one-hop paths) linked by a specified relationship type       |
| _/database/server_                          | Returns basic information on the UBKG neo4j database                                                     |
| _/node_types/counts_                        | Returns counts of nodes in the database by node type (label)                                             |
| _/node_types/counts/{node_type}_            | Returns counts of nodes in the database for a specified node type (label)                                |
| _/node_types/counts_by_sab_                 | Returns counts of nodes in the database for all node types (labels), grouped by source (SAB).See Note 1. |  
| _/node_types/counts_by_sab/{node_type}_     | Returns counts of nodes in the database for a specified node type (label), grouped by source (SAB).      |
| _/property_types_                           | Returns list of property types (keys)                                                                    |
| _/relationship_types_                       | Returns list of relationship types                                                                       |
| _/semantics/semantic_types_                 | Returns information on all Semantic Type nodes                                                           |
| _/semantics/semantic_types/{identifier}_    | Returns information on a specified Semantic Type                                                         |
| _/semantics/semantic_subtypes/{identifier}_ | Returns information on the set of Semantic Type nodes that are subtypes of the specified Semantic Type   |

##### Notes on new endpoints
1. When executed against a large UBKG instance, the execution time of the _/node_types/counts_by_sab_ endpoint will likely exceed the server host timeout. This endpoint exists as a convenience; a custom 400 message will explain the issue and suggest alternatives.

#### Deprecated endpoints

The following endpoints were part of the initial release of the ubkg-api, 
but have been deprecated. Cypher queries and model class files for the deprecated endpoints are 
archived in folders named **deprecated** in the appropriate folders.

Endpoints can be returned to the UBKG API if an appropriate use case is identified.

| Endpoint                          | Reason for deprecating                                |
|-----------------------------------|-------------------------------------------------------|
| _/concepts/<concept_id>/paths_    | Duplicates _/concepts/<concept_id>/paths/expand_      |
| _/tui/{tui_id}/semantics_         | Functionality now part of _/semantic_types_ endpoints |
| _/terms/{term_id}/concepts/terms_ | Incompatible with Cypher version 5                    |

# Known Limitations and Possible Enhancements

## Statistical endpoints
The current set of endpoints execute real-time Cypher queries. 
For very large UBKG instances (e.g., the Data Distillery), endpoints 
that calculate statistics such as count by type can result in errors of two types:
1. memory-related errors
2. timeout errors

Because a UBKG instance is static, it should be possible to calculate relevant
statistics during generation in some analytical structure (e.g., summary
tables). The UBKG API would then be able to obtain statistical information 
about a UBKG instance by consulting the relevant summary data instead of attempting to 
calculate in real time.

## Other potential enhancements
### _/paths_ endpoints based on Code nodes instead of Concept nodes
Examples include _/expand_ for a Code node, or  _/shortest_path_ endpoint between two Code nodes.
The challenge is the many:many relationship between Concept nodes and Code nodes. This requires
additional analysis.

### _/paths_ endpoints based on Semantic nodes
The challenge is that the subgraph of Semantic nodes appears to be cyclic.