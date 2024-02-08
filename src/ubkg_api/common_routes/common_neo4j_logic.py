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

import neo4j


from models.codes_codes_obj import CodesCodesObj
from models.concept_detail import ConceptDetail
from models.concept_prefterm import ConceptPrefterm
from models.concept_path import ConceptPath
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
# property class
from models.concept_prefterm import ConceptPrefterm


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

    Assumes that the file is in the cypher directory.
    """

    fpath = os.path.dirname(os.getcwd())
    fpath = os.path.join(fpath, 'ubkg_api/cypher', filename)

    f = open(fpath, "r")
    query = f.read()
    f.close()
    return query

def timebox_query(query: str, timeout: int=10000) -> str:

    """
    Limits the execution of a query to a specified timeout.
    :param query: query string to timebox
    :param timeout: timeout in ms. This can, for example, be set in the app.cfg file.
    """

    # Use simple string concatenation instead of an f-string to wrap the source query in a timebox call.
    return "CALL apoc.cypher.runTimeboxed('" + query + "',{}," + str(timeout) + ")"

def format_list_for_query(listquery: list[str], doublequote: bool =False) ->str:
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
    codesCodesObjs: List[CodesCodesObj] = []

    # JAS January 2024.
    # Fixed issue with SAB filtering.

    # Load Cypher query from file.
    query: str = loadquerystring(filename='codes_code_id_codes.cypher')

    # Filter by code_id.
    query = query.replace('$code_id',f"'{code_id}'")

    # Filter by code SAB.
    if len(sab) == 0:
        query = query.replace('$sabfilter','')
    else:
        query = query.replace('$sabfilter',f" AND c.SAB IN {sab}")

    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query, code_id=code_id, SAB=sab)
        for record in recds:
            try:
                codesCodesObj: CodesCodesObj = \
                    CodesCodesObj(record.get('Concept'), record.get('Code2'), record.get('Sab2')).serialize()
                codesCodesObjs.append(codesCodesObj)
            except KeyError:
                pass
    return codesCodesObjs


def codes_code_id_concepts_get_logic(neo4j_instance, code_id: str) -> List[ConceptDetail]:
    conceptDetails: List[ConceptDetail] = []

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
                conceptDetail: ConceptDetail = ConceptDetail(record.get('Concept'),
                                                             record.get('Prefterm')).serialize()
                conceptDetails.append(conceptDetail)
            except KeyError:
                pass
    return conceptDetails


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
    sabRelationshipConceptPrefterms: [SabRelationshipConceptPrefterm] = []
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
                sabRelationshipConceptPrefterm: SabRelationshipConceptPrefterm = \
                    SabRelationshipConceptPrefterm(record.get('SAB'), record.get('Relationship'),
                                                   record.get('Concept2'), record.get('Prefterm2')).serialize()
                sabRelationshipConceptPrefterms.append(sabRelationshipConceptPrefterm)
            except KeyError:
                pass
    return sabRelationshipConceptPrefterms


def concepts_concept_id_definitions_get_logic(neo4j_instance, concept_id: str) -> List[SabDefinition]:
    sabDefinitions: [SabDefinition] = []
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
                sabDefinition: SabDefinition = SabDefinition(record.get('SAB'),
                                                             record.get('Definition')).serialize()
                sabDefinitions.append(sabDefinition)
            except KeyError:
                pass
    return sabDefinitions


# JAS January 2024 Deprecated semantics routes.
"""
def concepts_concept_id_semantics_get_logic(neo4j_instance, concept_id) -> List[StyTuiStn]:
    styTuiStns: [StyTuiStn] = []
    query: str = \
        'WITH [$concept_id] AS query' \
        ' MATCH (a:Concept)-[:STY]->(b:Semantic)' \
        ' WHERE a.CUI IN query' \
        ' RETURN DISTINCT a.CUI AS concept, b.name AS STY, b.TUI AS TUI, b.STN as STN'
    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query, concept_id=concept_id)
        for record in recds:
            try:
                styTuiStn: StyTuiStn = StyTuiStn(record.get('STY'), record.get('TUI'),
                                                 record.get('STN')).serialize()
                styTuiStns.append(styTuiStn)
            except KeyError:
                pass
    return styTuiStns
"""
#  JAS February 2024: Refactored
def concepts_expand_get_logic(neo4j_instance, query_concept_id=None, sab=None, rel=None, mindepth=None,
                              maxdepth=None, skip=None, limit=None) -> List[ConceptPath]:
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

    conceptPaths: [ConceptPath] = []

    # Load query string and associate parameter values to variables.
    query=loadquerystring(filename='concepts_expand.cypher')
    query = query.replace('$query_concept_id',f'"{query_concept_id}"')
    sabjoin = format_list_for_query(listquery=sab, doublequote=True)
    query = query.replace('$sab', sabjoin)
    reljoin = format_list_for_query(listquery=rel, doublequote=True)
    query = query.replace('$rel', reljoin)
    query = query.replace('$mindepth', str(mindepth))
    query = query.replace('$maxdepth', str(maxdepth))
    query = query.replace('$skip', str(skip))
    query = query.replace('$limit', str(limit))

    # Limit query execution time to duration specified in app.cfg.
    query = timebox_query(query, timeout=neo4j_instance.timeout)

    path_position = int(skip)+1
    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)
        for record in recds:
            # The timebox query wraps each record in a dictionary with the record as the value of a key named 'value.'
            val = record.get('value')
            try:
                path_info = val.get('paths')
                # Add the position index for this path in the entire set--i.e., the row number from the query return,
                # based on the value of skip.
                path_info['position'] = path_position
                conceptPath: ConceptPath = ConceptPath(path_info=path_info).serialize()
                conceptPaths.append(conceptPath)
                path_position = path_position + 1
            except KeyError:
                pass

    return conceptPaths

# JAS February 2024 Deprecated, as the apoc.expandConfig call is identical to the apoc.expand.

# JAS January 2024 Converted from POST to GET
# def concepts_path_get_logic(neo4j_instance, query_concept_id=None, sab=None, rel=None ) -> List[PathItemConceptRelationshipSabPrefterm]:
#
#    """
#    :param neo4j_instance: UBKG connection
#    :param query_concept_id: CUI of concept from which to expand paths
#    :param sab: list of SABs by which to filter relationship types in the paths.
#    :param rel: list of relationship types by which to filter relationship types in the paths.
#    :param dept: maximum number of hops in the set of paths
#    """
#
#    pathItemConceptRelationshipSabPrefterms: [PathItemConceptRelationshipSabPrefterm] = []
#    query: str = \
#        "MATCH (c:Concept {CUI: $query_concept_id})" \
#        " CALL apoc.path.expandConfig(c, {relationshipFilter: apoc.text.join([x in [$rel] | '<'+x], ','),minLevel: size([$rel]),maxLevel: size([$rel])})" \
#        " YIELD path" \
#        " WHERE ALL(r IN relationships(path) WHERE r.SAB IN [$sab])" \
#        " WITH [n IN nodes(path) | n.CUI] AS concepts, [null]+[r IN relationships(path) |Type(r)] AS relationships, [null]+[r IN relationships(path) | r.SAB] AS sabs" \
#        " CALL{WITH concepts,relationships,sabs UNWIND RANGE(0, size(concepts)-1) AS items WITH items AS item, concepts[items] AS concept, relationships[items] AS relationship, sabs[items] AS sab RETURN COLLECT([item,concept,relationship,sab]) AS paths}" \
#        " WITH COLLECT(paths) AS rollup" \
#        " UNWIND RANGE(0, size(rollup)-1) AS path" \
#        " UNWIND rollup[path] as final" \
#        " OPTIONAL MATCH (:Concept{CUI:final[1]})-[:PREF_TERM]->(prefterm:Term)" \
#        " RETURN path as path, final[0] AS item, final[1] AS concept, final[2] AS relationship, final[3] AS sab, prefterm.name as prefterm"
#
#    sabjoin = format_list_for_query(sab)
#    query = query.replace('$sab', sabjoin)
#    reljoin = format_list_for_query(rel)
#    query = query.replace('$rel', reljoin)
#
#
#    with neo4j_instance.driver.session() as session:
#        recds: neo4j.Result = session.run(query,
#                                          query_concept_id=query_concept_id
#                                          )
#        for record in recds:
#            try:
#                pathItemConceptRelationshipSabPrefterm: PathItemConceptRelationshipSabPrefterm = \
#                    PathItemConceptRelationshipSabPrefterm(record.get('path'), record.get('item'),
#                                                           record.get('concept'), record.get('relationship'),
#                                                           record.get('sab'), record.get('prefterm')).serialize()
#                pathItemConceptRelationshipSabPrefterms.append(pathItemConceptRelationshipSabPrefterm)
#            except KeyError:
#               pass
#    return pathItemConceptRelationshipSabPrefterms

# JAS February 2024 - Refactored for v5.
# apoc.algo.dijkstraWithDefaultWeight was deprecated in version 5.
# Replaced the function with dijkstra, and accepted default weight.
def concepts_shortestpath_get_logic(neo4j_instance, origin_concept_id=None, terminus_concept_id=None,
                                     sab=None, rel=None) \
        -> List[PathItemConceptRelationshipSabPrefterm]:

    conceptPaths: [ConceptPath] = []

    # Load query string and associate parameter values to variables.
    query = loadquerystring(filename='concepts_shortestpath.cypher')
    query = query.replace('$origin_concept_id', f'"{origin_concept_id}"')
    query = query.replace('$terminus_concept_id', f'"{terminus_concept_id}"')
    sabjoin = format_list_for_query(listquery=sab, doublequote=True)
    query = query.replace('$sab', sabjoin)
    reljoin = format_list_for_query(listquery=rel, doublequote=True)
    query = query.replace('$rel', reljoin)
    # Limit query execution time to duration specified in app.cfg.
    query = timebox_query(query, timeout=neo4j_instance.timeout)

    path_position = 1
    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)
        for record in recds:
            # The timebox query wraps each record in a dictionary with the record as the value of a key named 'value.'
            val = record.get('value')
            try:
                path_info = val.get('paths')
                # Add the position index for this path in the entire set--i.e., the row number from the query return,
                # based on the value of skip.
                path_info['position'] = path_position
                conceptPath: ConceptPath = ConceptPath(path_info=path_info).serialize()
                conceptPaths.append(conceptPath)
                path_position = path_position + 1
            except KeyError:
                pass

    return conceptPaths

# JAS February 2024 Refactored to mirror concepts_expand_get_logic
def concepts_trees_get_logic(neo4j_instance, query_concept_id=None, sab=None, rel=None, mindepth=None,
                                  maxdepth=None, skip=None, limit=None) -> List[ConceptPath]:
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

    conceptPaths: [ConceptPath] = []

    # Load query string and associate parameter values to variables.
    query = loadquerystring(filename='concepts_spanning_tree.cypher')
    query = query.replace('$query_concept_id', f'"{query_concept_id}"')
    sabjoin = format_list_for_query(listquery=sab, doublequote=True)
    query = query.replace('$sab', sabjoin)
    reljoin = format_list_for_query(listquery=rel, doublequote=True)
    query = query.replace('$rel', reljoin)
    query = query.replace('$mindepth', str(mindepth))
    query = query.replace('$maxdepth', str(maxdepth))
    query = query.replace('$skip', str(skip))
    query = query.replace('$limit', str(limit))

    # Limit query execution time to duration specified in app.cfg.
    query = timebox_query(query, timeout=neo4j_instance.timeout)

    path_position = int(skip) + 1
    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)
        for record in recds:
            # The timebox query wraps each record in a dictionary with the record as the value of a key named 'value.'
            val = record.get('value')
            try:
                path_info = val.get('paths')
                # Add the position index for this path in the entire set--i.e., the row number from the query return,
                # based on the value of skip.
                path_info['position'] = path_position
                conceptPath: ConceptPath = ConceptPath(path_info=path_info).serialize()
                conceptPaths.append(conceptPath)
                path_position = path_position + 1
            except KeyError:
                pass

        return conceptPaths

def concepts_subgraph_get_logic(neo4j_instance, sab=None, rel=None, skip=None, limit=None) \
        -> List[ConceptPath]:
    """
    Obtains the set of concept pairs (one-hop paths) that involve relationships of specified types and defined by specified source
    SABs. For exammple, if sab="UBERON" and rel="part_of", then the endpoint returns all pairs of concepts
    with the part_of relationship defined by UBERON.

    :param neo4j_instance: UBKG connection
    :param sab: list of SABs by which to filter relationship types in the paths.
    :param rel: list of relationship types by which to filter relationship types in the paths.
    :param skip: paths to skip
    :param limit: maximum number of paths to return
    """

    conceptPaths: [ConceptPath] = []

    # Load query string and associate parameter values to variables.
    query=loadquerystring(filename='concepts_subgraph.cypher')
    sabjoin = format_list_for_query(listquery=sab, doublequote=True)
    query = query.replace('$sab', sabjoin)
    reljoin = format_list_for_query(listquery=rel, doublequote=True)
    query = query.replace('$rel', reljoin)
    query = query.replace('$skip', str(skip))
    query = query.replace('$limit', str(limit))

    # Limit query execution time to duration specified in app.cfg.
    query = timebox_query(query, timeout=neo4j_instance.timeout)

    path_position = int(skip)+1
    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)
        for record in recds:
            # The timebox query wraps each record in a dictionary with the record as the value of a key named 'value.'
            val = record.get('value')
            try:
                path_info = val.get('paths')
                # Add the position index for this path in the entire set--i.e., the row number from the query return,
                # based on the value of skip.
                path_info['position'] = path_position
                conceptPath: ConceptPath = ConceptPath(path_info=path_info).serialize()
                conceptPaths.append(conceptPath)
                path_position = path_position + 1
            except KeyError:
                pass

    return conceptPaths


def semantics_semantic_id_semantictypes_get_logic(neo4j_instance, types=None, skip=None, limit=None) -> List[SemanticType]:
    """
    Obtains information on the set of Semantic (semantic type) nodes that are subtypes (have ISA_STY relationships
    with) the semantic types identified in the types list.
    The list can contain two types of identifiers:
    1. Name (e.g., "Anatomical Structure")
    2. Type Unique Identifier (e.g., "T017")

    If types is empty, return all semantic types.

    :param types: a list string prepared by the controller.
    :param skip: SKIP value for the query
    :param limit: LIMIT value for the query

    """
    semantictypes: [SemanticType] = []
    # Load and parameterize base query.
    query = loadquerystring('semantics_semantictypes.cypher')

    if types is None:
        # Load all semantic types
        query = query.replace('$types','')
    else:
        typesjoin = format_list_for_query(listquery=types, doublequote=True)
        query = query.replace('$types', typesjoin)

    query = query.replace('$skip',str(skip))
    query = query.replace('$limit',str(limit))

    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)
        position = skip + 1
        for record in recds:
            semantic_type = record.get('semantic_type')
            try:
                semantictype: SemanticType = SemanticType(semantic_type,position).serialize()
                semantictypes.append(semantictype)
                position = position + 1
            except KeyError:
                pass
    return semantictypes

def terms_term_id_codes_get_logic(neo4j_instance, term_id: str) -> List[TermtypeCode]:

    termtypeCodes: [TermtypeCode] = []

    """
    Returns information on Codes with terms that exactly match the specified term_id string.
    """

    query: str = \
        'WITH [$term_id] AS query' \
        ' MATCH (a:Term)<-[b]-(c:Code)' \
        ' WHERE a.name IN query' \
        ' RETURN DISTINCT a.name AS Term, Type(b) AS TermType, c.CodeID AS Code' \
        ' ORDER BY Term, TermType, Code'

    # JAS February 2024
    # To prevent timeout errors, limit the query execution time to a value specified in the app.cfg.
    query = query.replace('$term_id', f'"{term_id}"')
    query = timebox_query(query,timeout=neo4j_instance.timeout)
    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)
        for record in recds:
            # The timeboxed query returns query results as values of a dict instead of as a dict.
            val = record.get('value')
            try:
                termtypeCode: TermtypeCode = TermtypeCode(val.get('TermType'), val.get('Code')).serialize()
                termtypeCodes.append(termtypeCode)
            except KeyError:
                pass
    return termtypeCodes

def terms_term_id_concepts_get_logic(neo4j_instance, term_id: str) -> List[str]:
    concepts: [str] = []
    query: str = \
        'WITH [$term_id] AS query' \
        ' MATCH (a:Term)<-[b]-(c:Code)<-[:CODE]-(d:Concept)' \
        ' WHERE a.name IN query AND b.CUI = d.CUI' \
        ' OPTIONAL MATCH (a:Term)<--(d:Concept) WHERE a.name IN query' \
        ' RETURN DISTINCT a.name AS Term, d.CUI AS Concept' \
        ' ORDER BY Concept ASC'

    # JAS February 2024
    # To prevent timeout errors, limit the query execution time to a value specified in the app.cfg.
    query = query.replace('$term_id', f'"{term_id}"')
    query = timebox_query(query, timeout=neo4j_instance.timeout)
    with neo4j_instance.driver.session() as session:
        recds: neo4j.Result = session.run(query)
        for record in recds:
            # The timeboxed query returns query results as values of a dict instead of as a dict.
            val = record.get('value')
            try:
                concept: str = val.get('Concept')
                concepts.append(concept)
            except KeyError:
                pass

    return concepts

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
# Deprecated semantic and tui routes
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
