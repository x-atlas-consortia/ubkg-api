from flask import Blueprint, jsonify, current_app

codes_blueprint = Blueprint('codes', __name__, url_prefix='/codes')


@codes_blueprint.route('/<code_id>/codes', methods=['GET'])
def codes_code_id_codes_get(code_id, sab=[]):
    """Returns a list of code_ids {Concept, Code, SAB} that code the same concept(s) as the code_id, optionally restricted to source (SAB)


    :param code_id: The code identifier
    :type code_id: str
    :param sab: One or more sources (SABs) to return
    :type sab: List[str]

    :rtype: Union[List[CodesCodesObj], Tuple[List[CodesCodesObj], int], Tuple[List[CodesCodesObj], int, Dict[str, str]]
    """
    return jsonify(current_app.neo4jManager.codes_code_id_codes_get(code_id, sab))


@codes_blueprint.route('/<code_id>/concepts', methods=['GET'])
def codes_code_id_concepts_get(code_id):
    """Returns a list of concepts {Concept, Prefterm} that the code_id codes


    :param code_id: The code identifier
    :type code_id: str

    :rtype: Union[List[ConceptDetail], Tuple[List[ConceptDetail], int], Tuple[List[ConceptDetail], int, Dict[str, str]]
    """
    return jsonify(current_app.neo4jManager.codes_code_id_concepts_get(code_id))
