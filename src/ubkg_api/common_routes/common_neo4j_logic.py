"""
January 2024
Refactored:
1. to work with neo4j version 5 Cypher
2. with new endpoints optimized for a fully-indexed v5 instance
3. to deprecate endpoints that either use deprecated Cypher or involve information limited to UMLS data (e.g.,
   semantic types and TUIs).
4. to replace all POST-based functions with GET-based functions.
5. to allow for timeboxing of queries that may exceed timeout (e.g., term searches)


"""
import logging
import re
from typing import List
import os

# Apr 2024
from pathlib import Path

import neo4j

from models.codes_codes_obj import CodesCodesObj
from models.concept_detail import ConceptDetail
from models.concept_graph import ConceptGraph
from models.concept_sab_rel_depth import ConceptSabRelDepth
from models.concept_term import ConceptTerm
from models.path_item_concept_relationship_sab_prefterm import PathItemConceptRelationshipSabPrefterm
# from models.qqst import QQST
from models.semantictype import SemanticType
from models.sab_definition import SabDefinition
from models.sab_relationship_concept_prefterm import SabRelationshipConceptPrefterm
from models.sab_relationship_concept_term import SabRelationshipConceptTerm
# JAS January 2024 Deprecqting semantic and tui models
# from models.semantic_stn import SemanticStn
# from models.sty_tui_stn import StyTuiStn
from models.termtype_code import TermtypeCode
from models.concept_prefterm import ConceptPrefterm
from models.concept_node import ConceptNode
from models.node_type import NodeType

logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s:%(lineno)d: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def loadquerystring(filename: str) -> str:
    """
    Loads a query string from a file.

    Keeping query strings separate from the Python code:
    1. Separates business logic from the presentation layer.
    2. Eases the transition from neo4j development to API development--in particular, by elminating the need to
         reformat a query string in Python

    :param filename: filename, without path.

    APRIL 2024
    Assumes that the file is in the cypher subdirectory, which is at the same level as the script path.
    When ubkg-api endpoints are called as passthrough from hs-ontology api, the script path is in hs-ontology-api.


    """

    #fpath = os.path.dirname(os.getcwd())
    #fpath = os.path.join(fpath, 'ubkg_api/cypher', filename)

    fpath = Path(__file__).resolve().parent.parent
    fpath = os.path.join(fpath,'cypher',filename)
    f = open(fpath, "r")
    query = f.read()
    f.close()
    return query


def timebox_query(query: str, timeout: int = 10000) -> str:

    """
    Limits the execution of a query to a specified timeout.
    :param query: query string to timebox
    :param timeout: timeout in ms. This can, for example, be set in the app.cfg file.
    """

    # Use simple string concatenation instead of an f-string to wrap the source query in a timebox call.
    return "CALL apoc.cypher.runTimeboxed('" + query + "',{}," + str(timeout) + ")"


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


def codes_code_id_codes_get_logic(neo4j_instance, code_id: str, sab: List[str]) -> List[CodesCodesObj]:
    """
    Returns the set of Code nodes that share Concept links with the specified Code node.
    :param neo4j_instance: neo4j connection
    :param code_id: CodeID for the Code node, in format <SAB>:<CODE>
    :param sab: optional list of SABs from which to select codes that share links to the Concept node linked to the
    Code node
    """
    codescodesobjs: List[CodesCodesObj] = []

    # JAS January 2024.
    # Fixed issue with SAB filtering.

    # Load Cypher query from file.
    query: str = loadquerystring(filename='codes_code_id_codes.cypher')

    # Filter by code_id.
    query = query.replace('$code_id', f"'{code_id}'")

    # Filter by code SAB.
    if len(sab) == 0:
        query = query.replace('$sabfilter', '')
    else:
        query = query.replace('$sabfilter', f" AND c.SAB IN {sab}")

    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query, code_id=code_id, SAB=sab)
        for record in recds:
            try:
                codescodesobj: CodesCodesObj = \
                    CodesCodesObj(record.get('Concept'), record.get('Code2'), record.get('Sab2')).serialize()
                codescodesobjs.append(codescodesobj)
            except KeyError:
                pass
    return codescodesobjs


def codes_code_id_concepts_get_logic(neo4j_instance, code_id: str) -> List[ConceptDetail]:
    conceptdetails: List[ConceptDetail] = []

    query: str = \
        'WITH [$code_id] AS query' \
        ' MATCH (a:Code)<-[:CODE]-(b:Concept)' \
        ' WHERE a.CodeID IN query' \
        ' OPTIONAL MATCH (b)-[:PREF_TERM]->(c:Term)' \
        ' RETURN DISTINCT a.CodeID AS Code, b.CUI AS Concept, c.name as Prefterm' \
        ' ORDER BY Code ASC, Concept'
    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query, code_id=code_id)
        for record in recds:
            try:
                conceptdetail: ConceptDetail = ConceptDetail(record.get('Concept'),
                                                             record.get('Prefterm')).serialize()
                conceptdetails.append(conceptdetail)
            except KeyError:
                pass
    return conceptdetails


# https://neo4j.com/docs/api/python-driver/current/api.html#explicit-transactions
def concepts_concept_id_codes_get_logic(neo4j_instance, concept_id: str, sab: List[str]) -> List[str]:
    codes: List[str] = []
    query: str = \
        'WITH [$concept_id] AS query' \
        ' MATCH (a:Concept)-[:CODE]->(b:Code)' \
        ' WHERE a.CUI IN query AND (b.SAB IN $SAB OR $SAB = [])' \
        ' RETURN DISTINCT a.CUI AS Concept, b.CodeID AS Code, b.SAB AS Sab' \
        ' ORDER BY Concept, Code ASC'
    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query, concept_id=concept_id, SAB=sab)
        for record in recds:
            try:
                code = record.get('Code')
                codes.append(code)
            except KeyError:
                pass
    return codes


def concepts_concept_id_concepts_get_logic(neo4j_instance, concept_id: str) -> List[SabRelationshipConceptTerm]:
    sabrelationshipconceptprefterms: [SabRelationshipConceptPrefterm] = []
    query: str = \
        'WITH [$concept_id] AS query' \
        ' MATCH (b:Concept)<-[c]-(d:Concept)' \
        ' WHERE b.CUI IN query' \
        ' OPTIONAL MATCH (b)-[:PREF_TERM]->(a:Term)' \
        ' OPTIONAL MATCH (d)-[:PREF_TERM]->(e:Term)' \
        ' RETURN DISTINCT a.name AS Prefterm1, b.CUI AS Concept1, c.SAB AS SAB, type(c) AS Relationship,' \
        '  d.CUI AS Concept2, e.name AS Prefterm2' \
        ' ORDER BY Concept1, Relationship, Concept2 ASC, Prefterm1, Prefterm2'
    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query, concept_id=concept_id)
        for record in recds:
            try:
                sabrelationshipconceptprefterm: SabRelationshipConceptPrefterm = \
                    SabRelationshipConceptPrefterm(record.get('SAB'), record.get('Relationship'),
                                                   record.get('Concept2'), record.get('Prefterm2')).serialize()
                sabrelationshipconceptprefterms.append(sabrelationshipconceptprefterm)
            except KeyError:
                pass
    return sabrelationshipconceptprefterms


def concepts_concept_id_definitions_get_logic(neo4j_instance, concept_id: str) -> List[SabDefinition]:
    sabdefinitions: [SabDefinition] = []
    query: str = \
        'WITH [$concept_id] AS query' \
        ' MATCH (a:Concept)-[:DEF]->(b:Definition)' \
        ' WHERE a.CUI in query' \
        ' RETURN DISTINCT a.CUI AS Concept, b.SAB AS SAB, b.DEF AS Definition' \
        ' ORDER BY Concept, SAB'
    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query, concept_id=concept_id)
        for record in recds:
            try:
                sabdefinition: SabDefinition = SabDefinition(record.get('SAB'),
                                                             record.get('Definition')).serialize()
                sabdefinitions.append(sabdefinition)
            except KeyError:
                pass
    return sabdefinitions

def get_graph(neo4j_instance, query: neo4j.Query) -> ConceptGraph:
    """
    Used by paths-related endpoints to return a graph object.
    :param query: query string with timeout
    :param neo4j_instance: UBKG connection

    Assumes that the query string returns a JSON object named graph in the nodes/paths/edges format.

    """
    conceptgraphs: [ConceptGraph] = []
    conceptgraph: ConceptGraph = {}

    with neo4j_instance.driver.session() as session:
        try:
            recds: neo4j.Result = session.run(query)
            for record in recds:
                graph = record.get('graph')
                try:
                    conceptgraph: ConceptGraph = ConceptGraph(graph=graph).serialize()
                    conceptgraphs.append(conceptgraph)
                except KeyError:
                    pass
        except neo4j.exceptions.ClientError as e:
            # If the error is from a timeout, return an empty value, to trigger the custom 404 message.
            if e.code == 'Neo.ClientError.Transaction.TransactionTimedOutClientConfiguration':
                return {}

    # There will be a maximum of one record.
    return conceptgraph

def concepts_expand_get_logic(neo4j_instance, query_concept_id=None, sab=None, rel=None, mindepth=None,
                              maxdepth=None, skip=None, limit=None) -> List[ConceptGraph]:
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
    """

    conceptgraphs: [ConceptGraph] = []
    conceptgraph: ConceptGraph = {}

    # Load query string and associate parameter values to variables.
    querytxt = loadquerystring(filename='concepts_expand.cypher')
    querytxt = querytxt.replace('$query_concept_id', f'"{query_concept_id}"')
    sabjoin = format_list_for_query(listquery=sab, doublequote=True)
    querytxt = querytxt.replace('$sab', sabjoin)
    reljoin = format_list_for_query(listquery=rel, doublequote=True)
    querytxt = querytxt.replace('$rel', reljoin)
    querytxt = querytxt.replace('$mindepth', str(mindepth))
    querytxt = querytxt.replace('$maxdepth', str(maxdepth))
    querytxt = querytxt.replace('$skip', str(skip))
    querytxt = querytxt.replace('$limit', str(limit))

    # Set timeout for query based on value in app.cfg.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    # MAY 2024 - bug fix - changed argument from querytxt to query
    return get_graph(neo4j_instance, query=query)

def concepts_shortestpath_get_logic(neo4j_instance, origin_concept_id=None, terminus_concept_id=None,
                                    sab=None, rel=None) \
        -> List[PathItemConceptRelationshipSabPrefterm]:

    # Load query string and associate parameter values to variables.
    querytxt = loadquerystring(filename='concepts_shortestpath.cypher')
    querytxt = querytxt.replace('$origin_concept_id', f'"{origin_concept_id}"')
    querytxt = querytxt.replace('$terminus_concept_id', f'"{terminus_concept_id}"')
    sabjoin = format_list_for_query(listquery=sab, doublequote=True)
    querytxt = querytxt.replace('$sab', sabjoin)
    reljoin = format_list_for_query(listquery=rel, doublequote=True)
    querytxt = querytxt.replace('$rel', reljoin)

    # Set timeout for query based on value in app.cfg.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    return get_graph(neo4j_instance, query=query)


# JAS February 2024 Refactored to mirror concepts_expand_get_logic
def concepts_trees_get_logic(neo4j_instance, query_concept_id=None, sab=None, rel=None, mindepth=None,
                             maxdepth=None, skip=None, limit=None) -> List[ConceptGraph]:
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
    """

    # Load query string and associate parameter values to variables.
    querytxt = loadquerystring(filename='concepts_spanning_tree.cypher')
    querytxt = querytxt.replace('$query_concept_id', f'"{query_concept_id}"')
    sabjoin = format_list_for_query(listquery=sab, doublequote=True)
    querytxt = querytxt.replace('$sab', sabjoin)
    reljoin = format_list_for_query(listquery=rel, doublequote=True)
    querytxt = querytxt.replace('$rel', reljoin)
    querytxt = querytxt.replace('$mindepth', str(mindepth))
    querytxt = querytxt.replace('$maxdepth', str(maxdepth))
    querytxt = querytxt.replace('$skip', str(skip))
    querytxt = querytxt.replace('$limit', str(limit))

    # Set timeout for query based on value in app.cfg.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    return get_graph(neo4j_instance, query=query)

def concepts_subgraph_get_logic(neo4j_instance, query_concept_id=None, sab=None, rel=None, skip=None, limit=None) \
        -> List[ConceptGraph]:
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

    # Limit query execution time to duration specified in app.cfg.
    # Set timeout for query based on value in app.cfg.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    return get_graph(neo4j_instance, query=query)

def semantics_semantic_id_semantic_types_get_logic(neo4j_instance, semtype=None, skip=None,
                                                   limit=None) -> List[SemanticType]:
    """
    Obtains information on the set of Semantic (semantic type) nodes that match the identifier semtype
    2. the set of Semantic (semantic type) nodes that are subtypes (have ISA_STY relationships
    with) the semantic type identified with semtype

    The identifier can contain be either of the following types of identifiers:
    1. Name (e.g., "Anatomical Structure")
    2. Type Unique Identifier (e.g., "T017")

    :param semtype: a string OR list string prepared by the controller.
    :param skip: SKIP value for the query
    :param limit: LIMIT value for the query
    :param neo4j_instance: neo4j connection

    """
    semantictypes: [SemanticType] = []
    # Load and parameterize base query.
    query = loadquerystring('semantics_semantic_types.cypher')

    # The query can handle a list of multiple type identifiers (with proper formatting using format_list_for_query) or
    # no values; however, the routes in the controller limit the type identifier to a single path variable.
    # Convert single value to a list with one element.
    if semtype is None:
        semtypes = []
    else:
        semtypes = [semtype]

    types = format_list_for_query(listquery=semtypes, doublequote=True)
    query = query.replace('$types', types)

    query = query.replace('$skip', str(skip))
    query = query.replace('$limit', str(limit))

    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)
        # Identify the absolute position of the semantic type in the return.
        position = int(skip) + 1
        for record in recds:
            # Each row from the query includes a dict that contains the actual response content.
            semantic_type = record.get('semantic_type')
            try:
                semantictype: SemanticType = SemanticType(semantic_type, position).serialize()
                semantictypes.append(semantictype)
                position = position + 1
            except KeyError:
                pass

    return semantictypes


def semantics_semantic_id_subtypes_get_logic(neo4j_instance, semtype=None, skip=None,
                                             limit=None) -> List[SemanticType]:
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
    semantictypes: [SemanticType] = []
    # Load and parameterize base query.
    query = loadquerystring('semantics_semantic_subtypes.cypher')

    # The query can handle a list of multiple type identifiers (with proper formatting using format_list_for_query) or
    # no values; however, the routes in the controller limit the type identifier to a single path variable.
    # Convert single value to a list with one element.
    if semtype is None:
        semtypes = []
    else:
        semtypes = [semtype]

    types = format_list_for_query(listquery=semtypes, doublequote=True)
    query = query.replace('$types', types)

    query = query.replace('$skip', str(skip))
    query = query.replace('$limit', str(limit))

    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)
        # Identify the absolute position of the semantic type in the return.
        position = int(skip) + 1
        for record in recds:
            # Each row from the query includes a dict that contains the actual response content.
            semantic_type = record.get('semantic_subtype')
            try:
                semantictype: SemanticType = SemanticType(semantic_type, position).serialize()
                semantictypes.append(semantictype)
                position = position + 1
            except KeyError:
                pass

    return semantictypes


def terms_term_id_codes_get_logic(neo4j_instance, term_id: str) -> List[TermtypeCode]:

    termtypecodes: [TermtypeCode] = []

    """
    Returns information on Codes with terms that exactly match the specified term_id string.
    """

    querytxt: str = \
        'WITH [$term_id] AS query' \
        ' MATCH (a:Term)<-[b]-(c:Code)' \
        ' WHERE a.name IN query' \
        ' RETURN DISTINCT a.name AS Term, Type(b) AS TermType, c.CodeID AS Code' \
        ' ORDER BY Term, TermType, Code'

    # JAS February 2024/May 2024
    # To prevent timeout errors, limit the query execution time to a value specified in the app.cfg
    querytxt = querytxt.replace('$term_id', f'"{term_id}"')

    # Set timeout for query based on value in app.cfg.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)
    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)
        for record in recds:
            try:
                termtypecode: TermtypeCode = TermtypeCode(record.get('TermType'), record.get('Code')).serialize()
                termtypecodes.append(termtypecode)
            except KeyError:
                pass
    return termtypecodes


def terms_term_id_concepts_get_logic(neo4j_instance, term_id: str) -> List[str]:
    concepts: [str] = []
    querytxt: str = \
        'WITH [$term_id] AS query' \
        ' MATCH (a:Term)<-[b]-(c:Code)<-[:CODE]-(d:Concept)' \
        ' WHERE a.name IN query AND b.CUI = d.CUI' \
        ' OPTIONAL MATCH (a:Term)<--(d:Concept) WHERE a.name IN query' \
        ' RETURN DISTINCT a.name AS Term, d.CUI AS Concept' \
        ' ORDER BY Concept ASC'

    # JAS February 2024/May 2024
    # To prevent timeout errors, limit the query execution time to a value specified in the app.cfg.
    querytxt = querytxt.replace('$term_id', f'"{term_id}"')

    # Set timeout for query based on value in app.cfg.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)
        for record in recds:
            try:
                concepts.append(record)
            except KeyError:
                pass

    return concepts


def remove_null_placeholder_objects(listdict: list[dict]) -> list[dict]:
    """
    If a Concept node identified in the query behind the concepts_identfier_node_get_logic does not have semantic types
    or definitions, the return will contain objects with null values--e.g.,
    "semantic_types": [
        {"def": null,
         "sty": null,
         "tui": null,
         "stn": null}
         ],
    "definitions": [
        {"def": null,
        "sab": null}
        ]

    This function removes the null objects from the list--e.g., to "semantic_types":[],"definitions":[]

    :param listdict: a list of dictionaries

    """

    listpop = []
    # Loop through the list and indentify placeholder dictionaries.
    for d in listdict:
        allnull = True
        for key, val in d.items():
            if val is not None:
                allnull = False
        if allnull:
            listpop.append(listdict.index(d))

    # Remove the placeholder dictionaries from the list.
    if len(listpop) > 0:
        for ld in listpop:
            listdict.pop(ld)

    return listdict


def concepts_identfier_node_get_logic(neo4j_instance, search: str) -> List[ConceptNode]:
    """
    Obtains information on the set of Concept subgraphs with identifiers that match the search parameter string.

    """
    # MAY 2024 - Replaced timeboxing method.

    conceptnodes: [ConceptNode] = []
    querytxt = loadquerystring(filename='concepts_nodes.cypher')

    # Format the search parameter for the Cypher query.
    list_identifier = [search]
    list_identifier_join = format_list_for_query(listquery=list_identifier, doublequote=True)
    querytxt = querytxt.replace('$search', list_identifier_join)

    # Set timeout for query based on value in app.cfg.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)
        for record in recds:
            concept = record.get('nodeobject')
            # Remove null placeholder dictionaries from nested list objects.
            concept['semantic_types'] = remove_null_placeholder_objects(concept.get('semantic_types'))
            concept['definitions'] = remove_null_placeholder_objects(concept.get('definitions'))
            try:
                conceptnode: ConceptNode = ConceptNode(concept).serialize()
                conceptnodes.append(conceptnode)
            except KeyError:
                pass

    return conceptnodes


def database_info_server_get_logic(neo4j_instance) -> dict:
    # Obtains neo4j database server information

    # The version was obtained from the instance at startup.
    dictret = {"version": neo4j_instance.database_version,
               # "name": neo4j_instance.database_name,
               "edition": neo4j_instance.database_edition}

    return dictret


# JAS January 2024
# Deprecating. The Cypher is incompatible with version 5.
"""
def terms_term_id_concepts_terms_get_logic(neo4j_instance, term_id: str) -> List[ConceptTerm]:
    conceptTerms: [ConceptTerm] = []
    query: str = \
        'WITH [$term_id] AS query' \
        ' OPTIONAL MATCH (a:Term)<-[b]-(c:Code)<-[:CODE]-(d:Concept)' \
        ' WHERE a.name IN query AND b.CUI = d.CUI' \
        ' OPTIONAL MATCH (a:Term)<--(d:Concept)' \
        ' WHERE a.name IN query WITH a,collect(d.CUI) AS next' \
        ' MATCH (f:Term)<-[:PREF_TERM]-(g:Concept)-[:CODE]->(h:Code)-[i]->(j:Term)' \
        ' WHERE g.CUI IN next AND g.CUI = i.CUI' \
        ' WITH a, g,COLLECT(j.name)+[f.name] AS x' \
        ' WITH * UNWIND(x) AS Term2' \
        ' RETURN DISTINCT a.name AS Term1, g.CUI AS Concept, Term2' \
        ' ORDER BY Term1, Term2'
    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query, term_id=term_id)
        for record in recds:
            try:
                conceptTerm: ConceptTerm = ConceptTerm(record.get('Concept'), record.get('Term2')).serialize()
                conceptTerms.append(conceptTerm)
            except KeyError:
                pass
    return conceptTerms
"""

# JAS January 2024
# Deprecated tui routes
"""
def tui_tui_id_semantics_get_logic(neo4j_instance, tui_id: str) -> List[SemanticStn]:
    semanticStns: [SemanticStn] = []
    query: str = \
        'WITH [$tui_id] AS query' \
        ' MATCH (a:Semantic)' \
        ' WHERE (a.TUI IN query OR query = [])' \
        ' RETURN DISTINCT a.name AS semantic, a.TUI AS TUI, a.STN AS STN1'
    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query, tui_id=tui_id)
        for record in recds:
            try:
                semanticStn: SemanticStn = SemanticStn(record.get('semantic'), record.get('STN1')).serialize()
                semanticStns.append(semanticStn)
            except KeyError:
                pass
    return semanticStns
"""


def node_types_node_type_counts_by_sab_get_logic(neo4j_instance, node_type=None, sab=None) -> dict:
    """
    Obtains information on node types, grouped by SAB.

    :param node_type: an optional filter for node type (label)
    :param neo4j_instance: neo4j connection
    :param sab: optional list of sabs

    """

    # MAY 2024 - Replaced timeboxing method.

    nodetypes: [NodeType] = []
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

    # Set timeout for query based on value in app.cfg.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)
        total_count = 0
        for record in recds:
            # Each row from the query includes a dict that contains the actual response content.
            output = record.get('output')
            node_types = output.get('node_types')
            for node_type in node_types:
                count_by_label = node_type.get('count')
                total_count = total_count + count_by_label
            try:
                nodetype: NodeType = NodeType(node_type).serialize()
                nodetypes.append(nodetype)
            except KeyError:
                pass

    dictret = {'total_count': total_count, 'node_types': nodetypes}
    return dictret


def node_types_node_type_counts_get_logic(neo4j_instance, node_type=None) -> dict:
    """
    Obtains information on node types.

    :param node_type: an optional filter for node type (label)
    :param neo4j_instance: neo4j connection

    """
    nodetypes: [NodeType] = []
    # Load and parameterize base query.
    querytxt = loadquerystring('node_types.cypher')

    if node_type is None:
        node_type = ''
    else:
        node_type = [node_type]
    typesjoin = format_list_for_query(listquery=node_type, doublequote=True)
    querytxt = querytxt.replace('$node_type', typesjoin)

    # MAY 2024 replaced timebox method.
    # Set timeout for query based on value in app.cfg.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)
        total_count = 0
        for record in recds:
            # Each row from the query includes a dict that contains the actual response content.
            output = record.get('output')
            node_types = output.get('node_types')
            print(node_types)
            for node_type in node_types:
                count_by_label = node_type.get('count')
                total_count = total_count + count_by_label
                try:
                    nodetype: NodeType = NodeType(node_type).serialize()
                    nodetypes.append(nodetype)
                except KeyError:
                    pass

    dictret = {'total_count': total_count, 'node_types': nodetypes}
    return dictret


def node_types_get_logic(neo4j_instance) -> dict:
    """
    Obtains information on node types.

    The return from the query is simple, and there is no need for a model class.

    :param neo4j_instance: neo4j connection

    """
    nodetypes: [dict] = []

    query = 'CALL db.labels() YIELD label RETURN apoc.coll.sort(COLLECT(label)) AS node_types'

    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)

        for record in recds:
            try:
                nodetype = record.get('node_types')
                nodetypes.append(nodetype)
            except KeyError:
                pass
    # The query returns a single record.
    dictret = {'node_types': nodetype}
    return dictret


def property_types_get_logic(neo4j_instance) -> dict:
    """
    Obtains information on property types.

    The return from the query is simple, and there is no need for a model class.

    :param neo4j_instance: neo4j connection

    """
    propertytypes: [dict] = []

    query = 'CALL db.propertyKeys() YIELD propertyKey RETURN apoc.coll.sort(COLLECT(propertyKey)) AS properties'

    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)

        for record in recds:
            try:
                propertytype = record.get('properties')
                propertytypes.append(propertytype)
            except KeyError:
                pass
    # The query returns a single record.
    dictret = {'property_types': propertytype}
    return dictret


def relationship_types_get_logic(neo4j_instance) -> dict:
    """
    Obtains information on relationship types.

    The return from the query is simple, and there is no need for a model class.

    :param neo4j_instance: neo4j connection

    """
    reltypes: [dict] = []

    query = 'CALL db.relationshipTypes() YIELD relationshipType ' \
            'RETURN apoc.coll.sort(COLLECT(relationshipType)) AS relationship_types'

    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)
        for record in recds:
            try:
                reltype = record.get('relationship_types')
                reltypes.append(reltype)
            except KeyError:
                pass

    # The query has a single record.
    dictret = {'relationship_types': reltype}
    return dictret


def sabs_get_logic(neo4j_instance) -> dict:
    """
    Obtains information on sources (SABs).

    The return from the query is simple, and there is no need for a model class.

    :param neo4j_instance: neo4j connection

    """
    sabs: [dict] = []

    # The commented version of the query results in a OOME.
    # query = 'MATCH (n:Code) RETURN apoc.coll.sort(COLLECT(n.SAB)) AS sab'
    query = 'CALL {match (n:Code) return distinct n.SAB AS sab ORDER BY sab} WITH COLLECT(sab) AS sabs RETURN sabs'

    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)

        for record in recds:
            try:
                sab = record.get('sabs')
                sabs.append(sab)
            except KeyError:
                pass
    # The query returns a single record.
    dictret = {'sabs': sab}
    return dictret


def sab_code_count_get(neo4j_instance, sab=None, skip=None, limit=None) -> dict:
    """
    Obtains information on SABs, including counts of codes associated with them.

    The return from the query is simple, and there is no need for a model class.

    :param neo4j_instance: neo4j connection
    :param skip: SKIP value for the query
    :param limit: LIMIT value for the query
    :param sab: identifier for a source (SAB)

    """
    sabs: [dict] = []

    # Load and parameterize query.
    query = loadquerystring('sabs_codes_counts.cypher')
    if sab is None:
        sabjoin = ''
    else:
        sabjoin = format_list_for_query(listquery=[sab], doublequote=True)
    query = query.replace('$sab', sabjoin)

    query = query.replace('$skip', str(skip))
    query = query.replace('$limit', str(limit))

    with neo4j_instance.driver.session() as session:
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

    # The query has a single record.
    dictret = {'sabs': sab}
    return dictret


def sab_code_detail_get(neo4j_instance, sab=None, skip=None, limit=None) -> dict:
    """
    Obtains information on the codes for a specified SAB, including counts.

    The return from the query is simple, and there is no need for a model class.

    :param neo4j_instance: neo4j connection
    :param skip: SKIP value for the query
    :param limit: LIMIT value for the query
    :param sab: source (SAB)

    """
    codes: [dict] = []

    # Load and parameterize query.
    querytxt = loadquerystring('sabs_codes_details.cypher')
    if sab is None:
        sabjoin = ''
    else:
        sabjoin = format_list_for_query(listquery=[sab], doublequote=True)
    querytxt = querytxt.replace('$sab', sabjoin)

    querytxt = querytxt.replace('$skip', str(skip))
    querytxt = querytxt.replace('$limit', str(limit))

    # MAY 2024 Replacing timebox method.
    # Set timeout for query based on value in app.cfg.
    query = neo4j.Query(text=querytxt, timeout=neo4j_instance.timeout)

    with neo4j_instance.driver.session() as session:
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

    # The query has a single record.
    dictret = {'codes': res_codes}
    return dictret


def sab_term_type_get_logic(neo4j_instance, sab=None, skip=None, limit=None) -> dict:
    """
    Obtains information on the term types of relationships between codes in a SAB.

    The return from the query is simple, and there is no need for a model class.

    :param neo4j_instance: neo4j connection
    :param skip: number of term types to skip
    :param limit: maximum number of term types to return
    :param sab: source (SAB)

    """
    termtypes: [dict] = []

    query = loadquerystring(filename='sabs_term_types.cypher')
    sabjoin = format_list_for_query(listquery=[sab], doublequote=True)
    query = query.replace('$sab', sabjoin)
    query = query.replace('$skip', str(skip))
    query = query.replace('$limit', str(limit))

    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)

        for record in recds:
            try:
                termtype = record.get('sabs')
                termtypes.append(termtype)
            except KeyError:
                pass
    # The query returns a single record.

    return termtype
