from flask import Blueprint, jsonify, current_app,make_response,request
from ..common_neo4j_logic import codes_code_id_codes_get_logic, codes_code_id_concepts_get_logic
from utils.http_error_string import get_404_error_string, validate_query_parameter_names, \
    validate_parameter_value_in_enum
from utils.http_parameter import parameter_as_list

codes_blueprint = Blueprint('codes', __name__, url_prefix='/codes')


@codes_blueprint.route('/<code_id>/codes', methods=['GET'])
def codes_code_id_codes_get(code_id, sab=None):
    """Returns a list of code_ids {Concept, Code, SAB} that code the same concept(s) as the code_id, optionally restricted to source (SAB)

    :param code_id: The code identifier
    :type code_id: str
    :param sab: One or more sources (SABs) to return. In the URL, sabs can be specified either with individual key-value pairs
    or a list delimited by a URL-escaped comma--e.g.,
    ?sab=SAB1&sab=SAB2
    or
    ?sab=SAB1%2CSAB2
    :type sab: List[str]

    :rtype: Union[List[CodesCodesObj], Tuple[List[CodesCodesObj], int], Tuple[List[CodesCodesObj], int, Dict[str, str]]
    """
    # Validate sab parameter.
    err = validate_query_parameter_names(['sab'])
    if err != 'ok':
        return make_response(err, 400)

    # Obtain a list of sab parameter values.
    sab = parameter_as_list(param_name='sab')

    neo4j_instance = current_app.neo4jConnectionHelper.instance()

    result = codes_code_id_codes_get_logic(neo4j_instance, code_id, sab)
    if result is None or result == []:
        # Empty result
        err = get_404_error_string(prompt_string='No codes sharing the Concept linked to the Code')
        return make_response(err, 404)

    return jsonify(result)


@codes_blueprint.route('/<code_id>/concepts', methods=['GET'])
def codes_code_id_concepts_get(code_id):
    """Returns a list of concepts {Concept, Prefterm} that the code_id codes

    :param code_id: The code identifier
    :type code_id: str

    :rtype: Union[List[ConceptDetail], Tuple[List[ConceptDetail], int], Tuple[List[ConceptDetail], int, Dict[str, str]]
    """
    neo4j_instance = current_app.neo4jConnectionHelper.instance()
    return jsonify(codes_code_id_concepts_get_logic(neo4j_instance, code_id))
