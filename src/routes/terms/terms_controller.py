from flask import Blueprint, jsonify

from neo4j_manager import get_neo4j_manager

terms_blueprint = Blueprint('terms', __name__, url_prefix='/terms')
neo4jManager = get_neo4j_manager()


@terms_blueprint.route('<term_id>/codes', methods=['GET'])
def terms_term_id_codes_get(term_id):  # noqa: E501
    """Returns a list of codes {TermType, Code} of the text string


    :param term_id: The term identifier
    :type term_id: str

    :rtype: Union[List[TermtypeCode], Tuple[List[TermtypeCode], int], Tuple[List[TermtypeCode], int, Dict[str, str]]
    """
    return jsonify(neo4jManager.terms_term_id_codes_get(term_id))


@terms_blueprint.route('<term_id>/concepts', methods=['GET'])
def terms_term_id_concepts_get(term_id):  # noqa: E501
    """Returns a list of concepts associated with the text string


    :param term_id: The term identifier
    :type term_id: str

    :rtype: Union[List[str], Tuple[List[str], int], Tuple[List[str], int, Dict[str, str]]
    """
    return jsonify(neo4jManager.terms_term_id_concepts_get(term_id))


@terms_blueprint.route('<term_id>/concepts/terms', methods=['GET'])
def terms_term_id_concepts_terms_get(term_id):  # noqa: E501
    """Returns an expanded list of concept(s) and preferred term(s) {Concept, Term} from an exact text match


    :param term_id: The term identifier
    :type term_id: str

    :rtype: Union[List[ConceptTerm], Tuple[List[ConceptTerm], int], Tuple[List[ConceptTerm], int, Dict[str, str]]
    """
    return jsonify(neo4jManager.terms_term_id_concepts_terms_get(term_id))
