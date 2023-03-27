from flask import Blueprint, jsonify

from neo4j_manager import get_neo4j_manager

concepts_blueprint = Blueprint('concepts', __name__, url_prefix='/concepts')
neo4jManager = get_neo4j_manager()


@concepts_blueprint.route('<concept_id>/codes', methods=['GET'])
def concepts_concept_id_codes_get(concept_id, sab=[]):  # noqa: E501
    """Returns a distinct list of code_id(s) that code the concept

     # noqa: E501

    :param concept_id: The concept identifier
    :type concept_id: str
    :param sab: One or more sources (SABs) to return
    :type sab: List[str]

    :rtype: Union[List[str], Tuple[List[str], int], Tuple[List[str], int, Dict[str, str]]
    """
    return jsonify(neo4jManager.concepts_concept_id_codes_get(concept_id, sab))


@concepts_blueprint.route('<concept_id>/concepts', methods=['GET'])
def concepts_concept_id_concepts_get(concept_id):  # noqa: E501
    """Returns a list of concepts {Sab, Relationship, Concept, Prefterm} related to the concept

     # noqa: E501

    :param concept_id: The concept identifier
    :type concept_id: str

    :rtype: Union[List[SabRelationshipConceptTerm], Tuple[List[SabRelationshipConceptTerm], int], Tuple[List[SabRelationshipConceptTerm], int, Dict[str, str]]
    """
    return jsonify(neo4jManager.concepts_concept_id_concepts_get(concept_id))


@concepts_blueprint.route('<concept_id>/definitions', methods=['GET'])
def concepts_concept_id_definitions_get(concept_id):  # noqa: E501
    """Returns a list of definitions {Sab, Definition} of the concept

     # noqa: E501

    :param concept_id: The concept identifier
    :type concept_id: str

    :rtype: Union[List[SabDefinition], Tuple[List[SabDefinition], int], Tuple[List[SabDefinition], int, Dict[str, str]]
    """
    return jsonify(neo4jManager.concepts_concept_id_definitions_get(concept_id))


@concepts_blueprint.route('<concept_id>/semantics', methods=['GET'])
def concepts_concept_id_semantics_get(concept_id):  # noqa: E501
    """Returns a list of semantic_types {Sty, Tui, Stn} of the concept

     # noqa: E501

    :param concept_id: The concept identifier
    :type concept_id: str

    :rtype: Union[List[StyTuiStn], Tuple[List[StyTuiStn], int], Tuple[List[StyTuiStn], int, Dict[str, str]]
    """
    return jsonify(neo4jManager.concepts_concept_id_semantics_get(concept_id))


@concepts_blueprint.route('expand', methods=['POST'])
def concepts_expand_post():  # noqa: E501
    """Returns a unique list of concepts (Concept, Preferred Term) on all paths including starting concept (query_concept_id) restricted by list of relationship types (rel), list of relationship sources (sab), and depth of travel.

     # noqa: E501

    :param concept_sab_rel_depth:
    :type concept_sab_rel_depth: dict | bytes

    :rtype: Union[List[ConceptPrefterm], Tuple[List[ConceptPrefterm], int], Tuple[List[ConceptPrefterm], int, Dict[str, str]]
    """
    if connexion.request.is_json:
        concept_sab_rel_depth = ConceptSabRelDepth.from_dict(connexion.request.get_json())  # noqa: E501
    return jsonify(neo4jManager.concepts_expand_post(concept_sab_rel_depth))


@concepts_blueprint.route('paths', methods=['POST'])
def concepts_path_post():  # noqa: E501
    """Return all paths of the relationship pattern specified within the selected sources

     # noqa: E501

    :param concept_sab_rel:
    :type concept_sab_rel: dict | bytes

    :rtype: Union[List[PathItemConceptRelationshipSabPrefterm], Tuple[List[PathItemConceptRelationshipSabPrefterm], int], Tuple[List[PathItemConceptRelationshipSabPrefterm], int, Dict[str, str]]
    """
    if connexion.request.is_json:
        concept_sab_rel = ConceptSabRel.from_dict(connexion.request.get_json())  # noqa: E501
    return jsonify(neo4jManager.concepts_path_post(concept_sab_rel))


@concepts_blueprint.route('shortestpath', methods=['POST'])
def concepts_shortestpaths_post():  # noqa: E501
    """Return all paths of the relationship pattern specified within the selected sources

     # noqa: E501

    :param qconcept_tconcept_sab_rel:
    :type qconcept_tconcept_sab_rel: dict | bytes

    :rtype: Union[List[PathItemConceptRelationshipSabPrefterm], Tuple[List[PathItemConceptRelationshipSabPrefterm], int], Tuple[List[PathItemConceptRelationshipSabPrefterm], int, Dict[str, str]]
    """
    if connexion.request.is_json:
        qconcept_tconcept_sab_rel = QconceptTconceptSabRel.from_dict(connexion.request.get_json())  # noqa: E501
    return jsonify(neo4jManager.concepts_shortestpaths_post(qconcept_tconcept_sab_rel))


@concepts_blueprint.route('trees', methods=['POST'])
def concepts_trees_post():  # noqa: E501
    """Return all paths of the relationship pattern specified within the selected sources

     # noqa: E501

    :param concept_sab_rel_depth:
    :type concept_sab_rel_depth: dict | bytes

    :rtype: Union[List[PathItemConceptRelationshipSabPrefterm], Tuple[List[PathItemConceptRelationshipSabPrefterm], int], Tuple[List[PathItemConceptRelationshipSabPrefterm], int, Dict[str, str]]
    """
    if connexion.request.is_json:
        concept_sab_rel_depth = ConceptSabRelDepth.from_dict(connexion.request.get_json())  # noqa: E501
    return jsonify(neo4jManager.concepts_trees_post(concept_sab_rel_depth))
