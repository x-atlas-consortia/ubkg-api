from flask import Blueprint, jsonify, current_app, make_response, request
from ..common_neo4j_logic import semantics_semantic_id_semantictypes_get_logic
from utils.http_error_string import get_404_error_string, validate_query_parameter_names, \
    validate_parameter_value_in_enum, validate_required_parameters, validate_parameter_is_numeric, \
    validate_parameter_is_nonnegative, validate_parameter_range_order, check_payload_size
from utils.http_parameter import parameter_as_list, set_default_minimum, set_default_maximum

semantics_blueprint = Blueprint('semantics', __name__, url_prefix='/semantics')


@semantics_blueprint.route('/semantictypes', methods=['GET'])
def semantics_semantic_id_semantics_get():
    """
    Returns a set of semantic types that are subtypes (have a IS_STY relationship with) the semantic types with
    identifiers in a specified list. Identifiers can be of two types:

    1. Name (e.g., "Anatomical Structure")
    2. Type Unique Identifier (TUI) (e.g., "T017")

    """
    neo4j_instance = current_app.neo4jConnectionHelper.instance()

    # Validate parameters.
    # Check for invalid parameter names.
    err = validate_query_parameter_names(parameter_name_list=['type', 'skip', 'limit'])
    if err != 'ok':
        return make_response(err, 400)

    # Check that the non-default skip is non-negative.
    skip = request.args.get('skip')
    err = validate_parameter_is_nonnegative(param_name='skip', param_value=skip)
    if err != 'ok':
        return make_response(err, 400)

    # Set default mininum.
    skip = set_default_minimum(param_value=skip, default=0)
    # Check that non-default limit is non-negative.
    limit = request.args.get('limit')
    err = validate_parameter_is_nonnegative(param_name='limit', param_value=limit)
    if err != 'ok':
        return make_response(err, 400)
    # Set default row limit, based on the app configuration.
    limit = set_default_maximum(param_value=limit, default=neo4j_instance.rowlimit)

    # Get remaining parameter values from the path or query string.
    types = parameter_as_list(param_name='type')

    result = semantics_semantic_id_semantictypes_get_logic(neo4j_instance, types=types, skip=skip, limit=limit)
    if result is None or result == []:
        # Empty result
        err = get_404_error_string(prompt_string=f"No Semantic Types")
        return make_response(err, 404)

    # Wrap origin and path list in a dictionary that will become the JSON response.
    dict_result = {'semantic_types':result}
    return jsonify(dict_result)

