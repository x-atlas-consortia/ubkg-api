"""
December 2025
Refactored:
1. To match a consistent pattern where an endpoint function loads its Cypher
   query from a file in the cypher path.
2. To work with a streamed response (usually JSON) from Cypher instead of
   translating the response into a "model" class.
3. To serialize neo4j Path objects in JSON format.

"""
import logging
import re
from typing import List
import os
import json

# For handling configurable timeouts
from werkzeug.exceptions import GatewayTimeout

# For serializing neo4j Path objects
from neo4j.graph import Path

from pathlib import Path

import neo4j

logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s:%(lineno)d: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

#--------------------
# UTILITY ROUTINES
# -------------------

def translate_query(session: neo4j.Session, querytxt: str, **params) -> str:
    """
    Returns a neo4j query string hydrated with parameter values.
    To be used for debugging or logging only.
    :param session: neo4j session
    :param params: parameter values
    :param querytxt: query string
    """

    display_query = querytxt
    for key, value in params.items():
        print(key, value)
        if isinstance(value, str):
            replacement = f"'{value}'"
        elif isinstance(value, list):
            replacement = json.dumps(value)
        elif value is None:
            replacement = 'null'
        else:
            replacement = str(value)
        display_query = display_query.replace(f'${key}', replacement)

    print('translate_query: ',display_query)
    return display_query

def loadquerystring(filename: str) -> str:
    """
    Loads a query string from a file.

    Keeping query strings separate from the Python code:
    1. Separates business logic from the presentation layer.
    2. Eases the transition from neo4j development to API development--in particular, by elminating the need to
         reformat a query string in Python

    :param filename: filename, without path.

    Assumes that the file is in the cypher subdirectory, which is at the same level as the script path.
    When ubkg-api endpoints are called as passthrough from hs-ontology api, the script path is in hs-ontology-api.


    """

    fpath = Path(__file__).resolve().parent.parent
    fpath = os.path.join(fpath,'cypher',filename)
    f = open(fpath, "r")
    query = f.read()
    f.close()
    return query


def format_list_for_query(listquery: list[str], doublequote: bool = False) -> str:

    """
    Converts a list of string values into a comma-delimited, delimited string for use in a Cypher query clause.
    :param listquery: list of string values
    :param doublequote: flag to set the delimiter.

    The default is a single quote; however, when a query
    is the argument for the apoc.timebox function, the delimiter should be double quote.

    Example:
        listquery: ['SNOMEDCT_US', 'HGNC']
        return:
            doublequote = False: "'SNOMEDCT_US', 'HGNC'"
            doublequote = True: '"SNOMEDCT_US","HGNC"'

    """
    if doublequote:
        return ', '.join('"{0}"'.format(s) for s in listquery)
    else:
        return ', '.join("'{0}'".format(s) for s in listquery)


def rel_str_to_array(rels: List[str]) -> List[List]:
    rel_array: List[List] = []
    for rel in rels:
        m = re.match(r'([^[]+)\[([^]]+)\]', rel)
        rel = m[1]
        sab = m[2]
        rel_array.append([rel, sab])
    return rel_array


# Each 'rel' list item is a string of the form 'Type[SAB]' which is translated into the array '[Type(t),t.SAB]'
# The Type or SAB can be a wild card '*', so '*[SAB]', 'Type[*]', 'Type[SAB]' and even '*[*]' are valid
def parse_and_check_rel(rel: List[str]) -> List[List]:
    try:
        rel_list: List[List] = rel_str_to_array(rel)
    except TypeError:
        raise Exception(f"The rel optional parameter must be of the form 'Type[SAB]', 'Type[*]', '*[SAB], or '*[*]'",
                        400)
    for r in rel_list:
        if not re.match(r"\*|[a-zA-Z_]+", r[0]):
            raise Exception(f"Invalid Type in rel optional parameter list", 400)
        if not re.match(r"\*|[a-zA-Z_]+", r[1]):
            raise Exception(f"Invalid SAB in rel optional parameter list", 400)
    return rel_list

#--------------------
# codes ENDPOINT ROUTINES
# -------------------

def codes_code_id_codes_get_logic(neo4j_instance, code_id: str, sab: List[str]) -> List[dict]:
    """
    Returns the set of Code nodes that share Concept links with the specified Code node.
    :param neo4j_instance: neo4j connection
    :param code_id: CodeID for the Code node, in format <SAB>:<CODE>
    :param sab: optional list of SABs from which to select codes that share links to the Concept node linked to the
    Code node

    # Assumption: the parameters code_id and sab were validated by the controller.
    """
    result: list[dict] = []

    # Load Cypher query template from file.
    querytxt: str = loadquerystring(filename='codes_code_id_codes.cypher')
    # The query template string contains placeholders:
    # $code_id, which corresponds to a neo4j parameter
    # $sabfilter, which corresponds to an optional filtering clause

    # BUILD QUERY PARAMS

    # Required filter on code_id.
    params: dict = {"code_id": code_id}

    # Optional filter by sab.
    # The values from term_type are passed as a Neo4j parameter.
    if len(sab) > 0:
        sab_clause = f" AND c.SAB IN $sabfilter"
        params["sabfilter"] = sab
    else:
        sab_clause = ""  # empty string replaces the placeholder

    # Update the query template with the optional sab filter.
    querytxt = querytxt.replace('$sabfilter', sab_clause)

    # Instantiate the query with the configured timeout.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with (neo4j_instance.driver.session() as session):
        try:
            # Execute the query with neo4j params
            recds: neo4j.Result = session.run(query, **params)

            for record in recds:
                result.append(record.get('codes'))

        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    # Because of the COLLECTS in the Cypher query, the response is a list that contains a list.
    # Return the inner list.
    return result[0]


def codes_code_id_concepts_get_logic(neo4j_instance, code_id: str) -> List[dict]:

    """
    Returns information on the Concept node that links to the specified Code node.
    :param neo4j_instance: neo4j connection
    :param code_id: CodeID for the Code node, in format <SAB>:<CODE>

    # Assumption: the parameter code_id was validated by the controller.

    """
    result: list[dict] = []

    # Load Cypher query template from file.
    querytxt: str = loadquerystring(filename='codes_code_id_concepts.cypher')

    # BUILD QUERY PARAMS

    # Required filter on code_id.
    params: dict = {"code_id": code_id}

    # Instantiate the query with the configured timeout.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        try:

            # Execute the query with neo4j params
            recds: neo4j.Result = session.run(query, **params)

            for record in recds:
                result.append(record.get('concepts'))


        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    # Because of the COLLECTS in the Cypher query, the response is a list that contains a list.
    # Return the inner list.
    return result[0]


def codes_code_id_terms_get_logic(neo4j_instance,code_id: str, term_type: list[str] | None = None) -> dict:
    """
    Obtains information on terms that link to a code.

    :param neo4j_instance: neo4j connection
    :param code_id: a UBKG Code in format SAB:CodeId
    :param term_type: an optional list of acronyms for a code type

    # Assumption: the parameters code_id and term_type were validated by the controller.
    """
    result: list[dict] = []

    # Load query template.
    querytxt = loadquerystring('code_code_id_terms.cypher')

    # The query template string contains placeholders:
    # $code_id, which corresponds to a neo4j parameter
    # $termtype_filter, which corresponds to an optional filtering clause

    # BUILD QUERY PARAMS

    # Required filter on code_id.
    params: dict = {"code_id": code_id}

    # Optional filter by term type.
    # The values from term_type are passed as a Neo4j parameter.
    if term_type:
        term_type_clause = "AND TYPE(r) IN $term_type_filter"
        params["term_type_filter"] = [t.upper() for t in term_type]
    else:
        term_type_clause = ""  # empty string replaces the placeholder

    # Update the query template with the optional term type filter.
    querytxt = querytxt.replace('$termtype_filter', term_type_clause)

    # Instantiate the query with the configured timeout.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:

        try:
            # Execute the query with neo4j params
            recds: neo4j.Result = session.run(query,**params)

            for record in recds:
                result.append(record.get('terms'))

        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    # Because of the COLLECTS in the Cypher query, the response is a list that contains a list.
    # Return the inner list.
    return result[0]

#--------------------
# concepts ENDPOINT ROUTINES
# -------------------

def concepts_concept_id_codes_get_logic(neo4j_instance, concept_id: str, sab: List[str]) -> List[str]:
    """
    Returns information on the Code nodes that link to the specified Concept node.
    :param neo4j_instance: neo4j connection
    :param concept_id: a Concept Unique Identifier (CUI)
    :param sab: a list of SAB codes by which to filter codes in response

    # Assumption: the parameter sab was validated by the controller.
    """

    result: list[str] = []

    # Load query template.
    querytxt: str = loadquerystring(filename='concepts_concept_id_codes.cypher')
    # The query template string contains placeholders:
    # $concept_id, which corresponds to a neo4j parameter
    # $sabfilter, which corresponds to an optional filtering clause

    # BUILD QUERY PARAMS

    # Required filter on concept_id.
    params: dict = {"concept_id": concept_id}

    #sabjoin = format_list_for_query(listquery=sab, doublequote=True)

    # Optional filter by sab.
    # The values from sab are passed as a Neo4j parameter.
    if len(sab) > 0:
        sab_clause = f" AND b.SAB IN $sabfilter"
        params["sabfilter"] = [s.upper() for s in sab]
    else:
        sab_clause = ""  # empty string replaces the placeholder

    # Update the query template with the optional sab filter.
    querytxt = querytxt.replace('$sabfilter', sab_clause)

    # Instantiate the query with the configured timeout.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        try:

            # Execute the query with neo4j params
            recds: neo4j.Result = session.run(query, **params)
            for record in recds:
                result.append(record.get('codes'))

        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    return result

def concepts_concept_id_concepts_get_logic(neo4j_instance, concept_id: str) -> List[dict]:
    """
    Returns information on the Concept nodes that have relationships with the
    specified concept.
    :param neo4j_instance: neo4j connection
    :param concept_id: a Concept Unique Identifier (CUI)

    """

    result: list[dict] = []

    # Load Cypher query template from file.
    querytxt: str = loadquerystring(filename='concepts_concept_id_concepts.cypher')
    # The query template string contains placeholders:
    # $concept_id, which corresponds to a neo4j parameter

    # BUILD QUERY PARAMS

    # Required filter on concept_id.
    params: dict = {"concept_id": concept_id}

    # Instantiate the query with the configured timeout.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        try:
            #recds: neo4j.Result = session.run(query)

            # Execute the query with neo4j params
            recds: neo4j.Result = session.run(query, **params)

            for record in recds:
                result.append(record.get('concepts'))

        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    # Because of the COLLECTS in the Cypher query, the response is a list that contains a list.
    # Return the inner list.
    return result[0]

def concepts_concept_id_definitions_get_logic(neo4j_instance, concept_id: str) -> List[dict]:
    """
    Returns information on the Definition nodes that link to the specified Concept node.
    :param neo4j_instance: neo4j connection
    :param concept_id: a Concept Unique Identifier (CUI)

    """

    result: list[dict] = []

    # Load Cypher query template from file.
    querytxt: str = loadquerystring(filename='concepts_concept_id_definitions.cypher')


    # BUILD QUERY PARAMS

    # Required filter on concept_id.
    params: dict = {"concept_id": concept_id}

    # Instantiate the query with the configured timeout.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        try:

            # Execute the query with neo4j params
            recds: neo4j.Result = session.run(query, **params)

            for record in recds:
                result.append(record.get('definitions'))

        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    # Because of the COLLECTS in the Cypher query, the response is a list that contains a list.
    # Return the inner list.
    return result[0]


def concepts_identifier_node_get_logic(neo4j_instance, search: str) -> List[dict]:
    """

    Obtains information on the set of Concept subgraphs (aka "Concept node objects")
    with identifiers that match the search parameter string.

    :param neo4j_instance: neo4j connection
    :param search: a search string

    """

    result: list[dict] = []

    # Load query string from file.
    querytxt = loadquerystring(filename='concepts_nodeobjects.cypher')

    # Format the search parameter for the Cypher query.
    list_identifier = [search]
    list_identifier_join = format_list_for_query(listquery=list_identifier, doublequote=True)
    querytxt = querytxt.replace('$search', list_identifier_join)

    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        try:
            recds: neo4j.Result = session.run(query)

            for record in recds:
                result.append(record.get('nodeobjects'))

        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    return {"nodeobjects":result}

#--------------------
# concepts/paths ENDPOINT UTILITIES
# -------------------

def get_graph(neo4j_instance, querytxt: str, **params) -> List[dict]:
    """

    Used by paths-related endpoints to return a graph object.
    :param querytxt: query string with timeout
    :param neo4j_instance: UBKG connection
    :param params: additional query parameters

    Assumes that the query string returns a JSON object named graph in the nodes/paths/edges format.

    """
    result: list[dict] = []

    # Instantiate the query with the configured timeout.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        try:
            #recds: neo4j.Result = session.run(query)
            debug_query = translate_query(session, querytxt=querytxt, **params)
            recds: neo4j.Result = session.run(query, **params)

            for record in recds:
                result.append(record.get('graph'))

        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    # There will be a maximum of one record.
    return result

#--------------------
# concepts/paths ENDPOINT ROUTINES
# -------------------
def concepts_expand_get_logic(neo4j_instance, query_concept_id=None, sab=None, rel=None, mindepth=None,
                              maxdepth=None, skip=None, limit=None) -> List[dict]:
    """

    Obtains a subset of paths that originate from the concept with CUI=query_concept_id, subject
    to constraints specified in parameters.

    :param neo4j_instance: UBKG connection
    :param query_concept_id: CUI of concept from which to expand paths
    :param sab: list of SABs by which to filter relationship types in the paths.
    :param rel: list of relationship types by which to filter relationship types in the paths.
    :param mindepth: minimum path length
    :param maxdepth: maximum path length
    :param skip: paths to skip
    :param limit: maximum number of paths to return

    Assumes that parameters were validated by the controller.
    """

    # Load query string template.
    querytxt = loadquerystring(filename='concepts_expand.cypher')

    # BUILD QUERY PARAMS
    params: dict = {"query_concept_id": query_concept_id,
                    "sab": sab,
                    "rel": rel,
                    "mindepth": int(mindepth),
                    "maxdepth": int(maxdepth),
                    "skip": int(skip),
                    "limit": int(limit)}

    # Return query as graph.
    return get_graph(neo4j_instance, querytxt=querytxt, **params)


def concepts_shortestpath_get_logic(neo4j_instance, origin_concept_id=None, terminus_concept_id=None,
                                    sab=None, rel=None) \
        -> List[dict]:
    """
    Returns the shortest path between two CUIs using Dykstra's algorithm with default weights,
    subject to constraints specified in parameters.

    Assumes that parameters were validated by the controller.
    """

    # Load query string template.
    querytxt = loadquerystring(filename='concepts_shortestpath.cypher')

    # BUILD QUERY PARAMS
    params: dict = {"origin_concept_id": origin_concept_id,
                    "terminus_concept_id": terminus_concept_id,
                    "sab": sab,
                    "rel": rel}

    # Return query as graph.
    return get_graph(neo4j_instance, querytxt=querytxt, **params)


def concepts_trees_get_logic(neo4j_instance, query_concept_id=None, sab=None, rel=None, mindepth=None,
                             maxdepth=None, skip=None, limit=None) -> List[dict]:
    """
    Obtains the spanning tree of paths that originate from the concept with CUI=query_concept_id, subject
    to constraints specified in parameters.

    :param neo4j_instance: UBKG connection
    :param query_concept_id: CUI of concept from which to expand paths
    :param sab: list of SABs by which to filter relationship types in the paths.
    :param rel: list of relationship types by which to filter relationship types in the paths.
    :param mindepth: minimum path length
    :param maxdepth: maximum path length
    :param skip: paths to skip
    :param limit: maximum number of paths to return

    Assumes that parameters were validated by the controller.
    """

    # Load query string template.
    querytxt = loadquerystring(filename='concepts_spanning_tree.cypher')

    # BUILD QUERY PARAMS
    params: dict = {"query_concept_id": query_concept_id,
                    "sab": sab,
                    "rel": rel,
                    "mindepth": int(mindepth),
                    "maxdepth": int(maxdepth),
                    "skip": int(skip),
                    "limit": int(limit)}

    # Return query as graph.
    return get_graph(neo4j_instance, querytxt=querytxt, **params)

#--------------------
# concepts/paths/subgraph ENDPOINT ROUTINES
# -------------------

def concepts_subgraph_get_logic(neo4j_instance, query_concept_id=None, sab=None, rel=None, skip=None, limit=None) \
        -> List[dict]:
    """
    Obtains the subgraph involving relationships of specified types and
    defined by specified source SABs. For exammple, if sab="UBERON" and rel="part_of", then the endpoint
    returns the subgraph  part_of relationship defined by UBERON.

    :param neo4j_instance: UBKG connection
    :param query_concept_id: CUI of originating concept of subgraph
    :param sab: list of SABs by which to filter relationship types in the paths.
    :param rel: list of relationship types by which to filter relationship types in the paths.
    :param skip: paths to skip
    :param limit: maximum number of paths to return
    """

    # Load query string and associate parameter values to variables.
    querytxt = loadquerystring(filename='concepts_subgraph.cypher')

    sabjoin = format_list_for_query(listquery=sab, doublequote=True)
    querytxt = querytxt.replace('$sab', sabjoin)
    reljoin = format_list_for_query(listquery=rel, doublequote=True)
    querytxt = querytxt.replace('$rel', reljoin)
    querytxt = querytxt.replace('$skip', str(skip))
    querytxt = querytxt.replace('$limit', str(limit))

    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    return get_graph(neo4j_instance, query=query)


def concepts_subgraph_sequential_get_logic(neo4j_instance, startCUI=None, reltypes=None, relsabs=None, skip=None,
                                           limit=None) -> List[dict]:

    """
    Obtains a subset of paths that originate from the concept with CUI=startCUI, in a sequence of relationships
    specified by reltypes and relsab, limited by skip and limit parameters.

    :param neo4j_instance: UBKG connection
    :param startCUI: CUI of concept from which to expand paths
    :param reltypes: sequential list of relationship types
    :param relsabs: sequential list of relationship SABs
    :param skip: paths to skip
    :param limit: maximum number of paths to return

    For example, reltypes=["isa","part_of"] and relsabs=["UBERON","PATO"] results in a query for paths that match
    the pattern

    (startCUI: Concept)-[r1:isa]-(c1:Concept)-[r2:has_part]->(c2:Concept)
    where r1.SAB = "UBERON" and r2.SAB="PATO"
    """

    # Load query string and associate parameter values to variables.
    querytxt = loadquerystring(filename='concepts_subgraph_sequential.cypher')
    querytxt = querytxt.replace('$startCUI', f'"{startCUI}"')

    sabjoin = format_list_for_query(listquery=reltypes, doublequote=True)
    querytxt = querytxt.replace('$reltypes', sabjoin)
    reljoin = format_list_for_query(listquery=relsabs, doublequote=True)
    querytxt = querytxt.replace('$relsabs', reljoin)
    querytxt = querytxt.replace('$skip', str(skip))
    querytxt = querytxt.replace('$limit', str(limit))

    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    return get_graph(neo4j_instance, query=query)


#--------------------
# semantics ENDPOINT ROUTINES
# -------------------

def semantics_semantic_id_semantic_types_get_logic(neo4j_instance, semtype=None, skip=None,
                                                   limit=None) -> List[dict]:
    """

    Obtains information on the set of
    1. Semantic (semantic type) nodes that match the identifier semtype
    2. the set of Semantic (semantic type) nodes that are subtypes (have ISA_STY relationships
    with) the semantic type identified with semtype

    The identifier can contain be either of the following types of identifiers:
    1. Name (e.g., "Anatomical Structure")
    2. Type Unique Identifier (e.g., "T017")

    :param neo4j_instance: UBKG connection
    :param semtype: a string OR list string prepared by the controller.
    :param skip: SKIP value for the query
    :param limit: LIMIT value for the query
    :param neo4j_instance: neo4j connection

    """
    result: list[dict] = []
    # Load and parameterize base query.
    querytxt = loadquerystring('semantics_semantic_types.cypher')

    # The query can handle a list of multiple type identifiers (with proper formatting using format_list_for_query) or
    # no values; however, the routes in the controller limit the type identifier to a single path variable.
    # Convert single value to a list with one element.
    if semtype is None:
        semtypes = []
    else:
        semtypes = [semtype]

    types = format_list_for_query(listquery=semtypes, doublequote=True)
    querytxt = querytxt.replace('$types', types)

    querytxt = querytxt.replace('$skip', str(skip))
    querytxt = querytxt.replace('$limit', str(limit))

    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        try:
            recds: neo4j.Result = session.run(query)

            # Add the relative position (skip) for each semantic type.
            position = int(skip) + 1
            for record in recds:
                semtypes = record.get('semantic_types')
                for semtype in semtypes:
                    typewithpos = dict(position=position)
                    typewithpos['semantic_type'] = semtype
                    position = position + 1
                    result.append(typewithpos)

        except neo4j.exceptions.ClientError as e:
             # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    return result


def semantics_semantic_id_subtypes_get_logic(neo4j_instance, semtype=None, skip=None,
                                             limit=None) -> List[dict]:
    """

    Obtains information on the set of Semantic (semantic type) nodes that match the set of Semantic (semantic type)
    nodes that are subtypes (have ISA_STY relationships with) the semantic type identified with semtype

    The identifier can contain be either of the following types of identifiers:
    1. Name (e.g., "Anatomical Structure")
    2. Type Unique Identifier (e.g., "T017")

    :param semtype: a string OR list string prepared by the controller.
    :param skip: SKIP value for the query
    :param limit: LIMIT value for the query
    :param neo4j_instance: neo4j connection

    """
    result: list[dict] = []
    # Load and parameterize base query.
    querytxt = loadquerystring('semantics_semantic_subtypes.cypher')

    # The query can handle a list of multiple type identifiers (with proper formatting using format_list_for_query) or
    # no values; however, the routes in the controller limit the type identifier to a single path variable.
    # Convert single value to a list with one element.
    if semtype is None:
        semtypes = []
    else:
        semtypes = [semtype]

    types = format_list_for_query(listquery=semtypes, doublequote=True)
    querytxt = querytxt.replace('$types', types)

    querytxt = querytxt.replace('$skip', str(skip))
    querytxt = querytxt.replace('$limit', str(limit))

    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        try:
            recds: neo4j.Result = session.run(query)

            # Add the relative position (skip) for each semantic subtype.
            position = int(skip) + 1
            for record in recds:
                subtypes = record.get('semantic_subtypes')
                for subtype in subtypes:
                    subtypewithpos = dict(position=position)
                    subtypewithpos['semantic_type'] = subtype
                    position = position + 1
                    result.append(subtypewithpos)


        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    return result

#--------------------
# terms ENDPOINT ROUTINES
# -------------------

def terms_term_id_codes_get_logic(neo4j_instance, term_id: str) -> List[dict]:

    result: list[dict] = []

    """
    
    Returns information on Codes with terms that exactly match the specified term_id string.
    """

    # Load and parameterize base query.
    querytxt = loadquerystring('terms_term_id_codes.cypher')
    querytxt = querytxt.replace('$term_id', f'"{term_id}"')

    # Set timeout for query based on value in app.cfg.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        try:
            recds: neo4j.Result = session.run(query)

            for record in recds:
                result.append(record.get('codes'))

        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    return result

def terms_term_id_concepts_get_logic(neo4j_instance, term_id: str) -> List[str]:

    """
    Returns information on Concepts with preferred terms that match the specified term_id string.
    """

    concepts: list[str] = []
    querytxt = loadquerystring('terms_term_id_concepts.cypher')

    querytxt = querytxt.replace('$term_id', f'"{term_id}"')

    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    # The Cypher query is not in JSON format, but is a list of lists.
    # Maintain for downward compatibility.
    with neo4j_instance.driver.session() as session:
        try:
            recds: neo4j.Result = session.run(query)
            for record in recds:
                try:
                    concepts.append(record)
                except KeyError:
                    pass
        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    return concepts

#--------------------
# general ENDPOINT ROUTINES
# -------------------

def database_info_server_get_logic(neo4j_instance) -> dict:
    # Obtains neo4j database server information

    # The version was obtained from the instance at startup.
    dictret = {"version": neo4j_instance.database_version,
               # "name": neo4j_instance.database_name,
               "edition": neo4j_instance.database_edition}

    return dictret

def property_types_get_logic(neo4j_instance) -> dict:
    """

    Obtains information on property types.

    :param neo4j_instance: neo4j connection

    """
    result: list[dict] = []

    querytxt = loadquerystring('property_types.cypher')

    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        with neo4j_instance.driver.session() as session:
            try:
                recds: neo4j.Result = session.run(query)
                for record in recds:
                    result.append(record.get('property_types'))

            except neo4j.exceptions.ClientError as e:
                # If the error is from a timeout, raise a HTTP 408.
                if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                    raise GatewayTimeout

        # The query returns a list of a list.
        return {'property_types': result[0]}


def relationship_types_get_logic(neo4j_instance) -> dict:
    """
    Obtains information on relationship types.

    :param neo4j_instance: neo4j connection

    """
    result: list[dict] = []

    querytxt = loadquerystring('relationship_types.cypher')

    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        with neo4j_instance.driver.session() as session:
            try:
                recds: neo4j.Result = session.run(query)
                for record in recds:
                    result.append(record.get('relationship_types'))

            except neo4j.exceptions.ClientError as e:
                # If the error is from a timeout, raise a HTTP 408.
                if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                    raise GatewayTimeout

        # The query returns a list of a list.
        return {'relationship_types': result[0]}

def sources_get_logic(neo4j_instance, sab=None, context=None) -> dict:
    """
    Obtains information on sources, or nodes in the UBKGSOURCE ontology.

    :param neo4j_instance: neo4j connection
    :param sab: source (SAB)
    :param context: UBKG context

    """
    sources: list[dict] = []

    # Load and parameterize query.
    querytxt = loadquerystring('sources.cypher')
    # Filter by code SAB.
    if len(sab) == 0:
        querytxt = querytxt.replace('$sabfilter', '')
    else:
        querytxt = querytxt.replace('$sabfilter', f" AND t.name IN {sab}")

    # Filter by ubkg context.
    if len(context) == 0:
        querytxt = querytxt.replace('$contextfilter', '')
    else:
        querytxt = querytxt.replace('$contextfilter', f" AND tContext.name IN {context}")

    # Set timeout for query based on value in app.cfg.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        try:
            recds: neo4j.Result = session.run(query)
            for record in recds:

                source = record.get('response')
                try:
                    sources.append(source)

                except KeyError:
                    pass
        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    return source

#--------------------
# node-types ENDPOINT ROUTINES
# -------------------

def node_types_node_type_counts_by_sab_get_logic(neo4j_instance, node_type=None, sab=None) -> dict:
    """
    Obtains information on node types, grouped by SAB.

    :param node_type: an optional filter for node type (label)
    :param neo4j_instance: neo4j connection
    :param sab: optional list of sabs

    """

    nodetypes: list[dict] = []
    # Load and parameterize base query.
    querytxt = loadquerystring('node_types_by_sab.cypher')

    if node_type is None:
        node_type = ''
    else:
        node_type = [node_type]
    typesjoin = format_list_for_query(listquery=node_type, doublequote=True)
    querytxt = querytxt.replace('$node_type', typesjoin)

    if sab is None:
        sab = ''
    else:
        sabjoin = format_list_for_query(listquery=sab, doublequote=True)
    querytxt = querytxt.replace('$sab', sabjoin)

    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        try:
            recds: neo4j.Result = session.run(query)
            total_count = 0
            for record in recds:
                # Each row from the query includes a dict that contains the actual response content.
                output = record.get('output')
                node_types = output.get('node_types')
                for node_type in node_types:
                    count_by_label = node_type.get('count')
                    total_count = total_count + count_by_label
                    nodetypes.append({'node_type':node_type})
        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    dictret = {'total_count': total_count, 'node_types': nodetypes}
    return dictret


def node_types_node_type_counts_get_logic(neo4j_instance, node_type=None) -> dict:
    """

    Obtains information on node types.

    :param node_type: an optional filter for node type (label)
    :param neo4j_instance: neo4j connection

    """
    nodetypes: list[dict] = []
    # Load and parameterize base query.

    querytxt = loadquerystring('node_types_counts.cypher')

    if node_type is None:
        node_type = ''
    else:
        node_type = [node_type]
    typesjoin = format_list_for_query(listquery=node_type, doublequote=True)
    querytxt = querytxt.replace('$node_type', typesjoin)

    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        try:
            recds: neo4j.Result = session.run(query)
            total_count = 0
            for record in recds:
                # Each row from the query includes a dict that contains the actual response content.
                output = record.get('output')
                node_types = output.get('node_types')
                for node_type in node_types:
                    count_by_label = node_type.get('count')
                    total_count = total_count + count_by_label
                    nodetypes.append({'node_type': node_type})

        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    dictret = {'total_count': total_count, 'node_types': nodetypes}
    return dictret


def node_types_get_logic(neo4j_instance) -> dict:
    """

    Obtains information on node types.

    :param neo4j_instance: neo4j connection

    """
    result: list[dict] = []

    querytxt = loadquerystring('node_types.cypher')

    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        try:
            recds: neo4j.Result = session.run(query)
            for record in recds:
                result.append(record.get('node_types'))

        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    # The query returns a list of a list.
    return {'node_types':result[0]}

#--------------------
# sabs ENDPOINT ROUTINES
# -------------------

def sabs_get_logic(neo4j_instance) -> dict:
    """
    Obtains information on sources (SABs).

    :param neo4j_instance: neo4j connection

    """
    sabs: list[dict] = []

    # The commented version of the query results in a OOME.
    # query = 'MATCH (n:Code) RETURN apoc.coll.sort(COLLECT(n.SAB)) AS sab'
    querytxt = loadquerystring('sabs.cypher')

    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        try:
            recds: neo4j.Result = session.run(query)

            for record in recds:
                try:
                    sab = record.get('sabs')
                    sabs.append(sab)
                except KeyError:
                    pass
        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    # The query returns a single record.
    dictret = {'sabs': sab}
    return dictret


def sabs_codes_counts_query_get(neo4j_instance, sab=None, skip=None, limit=None) -> dict:
    """
    Obtains information on SABs, including counts of codes associated with them.

    :param neo4j_instance: neo4j connection
    :param skip: SKIP value for the query
    :param limit: LIMIT value for the query
    :param sab: identifier for a source (SAB)

    """
    sabs: list[dict] = []

    # Load and parameterize query.
    querytxt = loadquerystring('sabs_codes_counts.cypher')
    if sab is None:
        sabjoin = ''
    else:
        sabjoin = format_list_for_query(listquery=[sab], doublequote=True)
    querytxt = querytxt.replace('$sab', sabjoin)

    querytxt = querytxt.replace('$skip', str(skip))
    querytxt = querytxt.replace('$limit', str(limit))

    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)
    with neo4j_instance.driver.session() as session:
        try:
            recds: neo4j.Result = session.run(query)

            # Track the position of the sabs in the list, based on the value of skip.
            position = int(skip) + 1
            for record in recds:
                try:
                    sab = record.get('sabs')
                    for s in sab:
                        s['position'] = position
                        position = position + 1
                    sabs.append(sab)

                except KeyError:
                    pass
        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    # The query has a single record.
    dictret = {'sabs': sab}
    return dictret


def sab_code_detail_query_get(neo4j_instance, sab=None, skip=None, limit=None) -> dict:
    """
    Obtains information on the codes for a specified SAB, including counts.


    :param neo4j_instance: neo4j connection
    :param skip: SKIP value for the query
    :param limit: LIMIT value for the query
    :param sab: source (SAB)

    """
    codes: list[dict] = []

    # Load and parameterize query.
    querytxt = loadquerystring('sabs_codes_details.cypher')
    if sab is None:
        sabjoin = ''
    else:
        sabjoin = format_list_for_query(listquery=[sab], doublequote=True)
    querytxt = querytxt.replace('$sab', sabjoin)

    querytxt = querytxt.replace('$skip', str(skip))
    querytxt = querytxt.replace('$limit', str(limit))

    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        try:
            recds: neo4j.Result = session.run(query)
            # Track the position of the codes in the list, based on the value of skip.
            position = int(skip) + 1
            res_codes = {}
            for record in recds:
                output = record.get('output')
                try:
                    res_codes = output.get('codes')
                    for c in res_codes:
                        c['position'] = position
                        position = position + 1
                    codes.append(res_codes)

                except KeyError:
                    pass
        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    # The query has a single record.
    dictret = {'codes': res_codes}
    return dictret

def sab_term_type_get_logic(neo4j_instance, sab=None, skip=None, limit=None) -> dict:
    """
    Obtains information on the term types of relationships between codes in a SAB.

    :param neo4j_instance: neo4j connection
    :param skip: number of term types to skip
    :param limit: maximum number of term types to return
    :param sab: source (SAB)

    """
    termtypes: list[dict] = []

    querytxt = loadquerystring(filename='sabs_term_types.cypher')
    sabjoin = format_list_for_query(listquery=[sab], doublequote=True)
    querytxt = querytxt.replace('$sab', sabjoin)
    querytxt = querytxt.replace('$skip', str(skip))
    querytxt = querytxt.replace('$limit', str(limit))

    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        try:
            recds: neo4j.Result = session.run(query)

            for record in recds:
                try:
                    termtype = record.get('sabs')
                    termtypes.append(termtype)
                except KeyError:
                    pass
        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, raise a HTTP 408.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                raise GatewayTimeout

    # The query returns a single record.

    return termtype