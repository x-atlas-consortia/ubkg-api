from flask import Blueprint, jsonify, current_app, request

from models.concept_sab_rel import ConceptSabRel
from models.concept_sab_rel_depth import ConceptSabRelDepth
from models.qconcept_tconcept_sab_rel import QconceptTconceptSabRel

concepts_blueprint = Blueprint('concepts', __name__, url_prefix='/concepts')


@concepts_blueprint.route('<concept_id>/codes', methods=['GET'])
def concepts_concept_id_codes_get(concept_id, sab=[]):
    """Returns a distinct list of code_id(s) that code the concept


    :param concept_id: The concept identifier
    :type concept_id: str
    :param sab: One or more sources (SABs) to return
    :type sab: List[str]

    :rtype: Union[List[str], Tuple[List[str], int], Tuple[List[str], int, Dict[str, str]]
    """
    return jsonify(current_app.neo4jManager.concepts_concept_id_codes_get(concept_id, sab))


@concepts_blueprint.route('<concept_id>/concepts', methods=['GET'])
def concepts_concept_id_concepts_get(concept_id):
    """Returns a list of concepts {Sab, Relationship, Concept, Prefterm} related to the concept


    :param concept_id: The concept identifier
    :type concept_id: str

    :rtype: Union[List[SabRelationshipConceptTerm], Tuple[List[SabRelationshipConceptTerm], int], Tuple[List[SabRelationshipConceptTerm], int, Dict[str, str]]
    """
    return jsonify(current_app.neo4jManager.concepts_concept_id_concepts_get(concept_id))


@concepts_blueprint.route('<concept_id>/definitions', methods=['GET'])
def concepts_concept_id_definitions_get(concept_id):
    """Returns a list of definitions {Sab, Definition} of the concept


    :param concept_id: The concept identifier
    :type concept_id: str

    :rtype: Union[List[SabDefinition], Tuple[List[SabDefinition], int], Tuple[List[SabDefinition], int, Dict[str, str]]
    """
    return jsonify(current_app.neo4jManager.concepts_concept_id_definitions_get(concept_id))


@concepts_blueprint.route('<concept_id>/semantics', methods=['GET'])
def concepts_concept_id_semantics_get(concept_id):
    """Returns a list of semantic_types {Sty, Tui, Stn} of the concept


    :param concept_id: The concept identifier
    :type concept_id: str

    :rtype: Union[List[StyTuiStn], Tuple[List[StyTuiStn], int], Tuple[List[StyTuiStn], int, Dict[str, str]]
    """
    return jsonify(current_app.neo4jManager.concepts_concept_id_semantics_get(concept_id))


@concepts_blueprint.route('expand', methods=['POST'])
def concepts_expand_post():
    """Returns a unique list of concepts (Concept, Preferred Term) on all paths including starting concept (query_concept_id) restricted by list of relationship types (rel), list of relationship sources (sab), and depth of travel.


    :param concept_sab_rel_depth:
    :type concept_sab_rel_depth: dict | bytes

    :rtype: Union[List[ConceptPrefterm], Tuple[List[ConceptPrefterm], int], Tuple[List[ConceptPrefterm], int, Dict[str, str]]
    """
    concept_sab_rel_depth = ConceptSabRelDepth.from_dict(request.get_json())
    return jsonify(current_app.neo4jManager.concepts_expand_post(concept_sab_rel_depth))


@concepts_blueprint.route('paths', methods=['POST'])
def concepts_path_post():
    """Return all paths of the relationship pattern specified within the selected sources


    :param concept_sab_rel:
    :type concept_sab_rel: dict | bytes

    :rtype: Union[List[PathItemConceptRelationshipSabPrefterm], Tuple[List[PathItemConceptRelationshipSabPrefterm], int], Tuple[List[PathItemConceptRelationshipSabPrefterm], int, Dict[str, str]]
    """
    concept_sab_rel = ConceptSabRel.from_dict(request.get_json())
    return jsonify(current_app.neo4jManager.concepts_path_post(concept_sab_rel))


@concepts_blueprint.route('shortestpaths', methods=['POST'])
def concepts_shortestpaths_post():
    """Return all paths of the relationship pattern specified within the selected sources


    :param qconcept_tconcept_sab_rel:
    :type qconcept_tconcept_sab_rel: dict | bytes

    :rtype: Union[List[PathItemConceptRelationshipSabPrefterm], Tuple[List[PathItemConceptRelationshipSabPrefterm], int], Tuple[List[PathItemConceptRelationshipSabPrefterm], int, Dict[str, str]]
    """
    qconcept_tconcept_sab_rel = QconceptTconceptSabRel.from_dict(request.get_json())
    return jsonify(current_app.neo4jManager.concepts_shortestpaths_post(qconcept_tconcept_sab_rel))


@concepts_blueprint.route('trees', methods=['POST'])
def concepts_trees_post():
    """Return all paths of the relationship pattern specified within the selected sources


    :param concept_sab_rel_depth:
    :type concept_sab_rel_depth: dict | bytes

    :rtype: Union[List[PathItemConceptRelationshipSabPrefterm], Tuple[List[PathItemConceptRelationshipSabPrefterm], int], Tuple[List[PathItemConceptRelationshipSabPrefterm], int, Dict[str, str]]
    """
    concept_sab_rel_depth = ConceptSabRelDepth.from_dict(request.get_json())
    return jsonify(current_app.neo4jManager.concepts_trees_post(concept_sab_rel_depth))
