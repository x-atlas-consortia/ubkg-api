from flask import Blueprint, jsonify, current_app, make_response, request
from ..common_neo4j_logic import semantics_semantic_id_semantic_get_logic
from utils.http_error_string import get_404_error_string, validate_query_parameter_names, \
    validate_parameter_value_in_enum, validate_required_parameters, validate_parameter_is_numeric, \
    validate_parameter_is_nonnegative, validate_parameter_range_order, check_payload_size
from utils.http_parameter import parameter_as_list, set_default_minimum, set_default_maximum

semantics_blueprint = Blueprint('semantics', __name__, url_prefix='/semantics')

@semantics_blueprint.route('semantic_types', methods=['GET'])
def semantics_semantic_types_get():
    # Return information on all semantic types.
    return semantics_semantic_get(identifier=None, isforsubtypes=False)

@semantics_blueprint.route('<identifier>/semantic_types', methods=['GET'])
def semantics_identifier_semantic_types_get(identifier):
    # Return information on specified semantic type.
    return semantics_semantic_get(identifier, isforsubtypes=False)

@semantics_blueprint.route('<identifier>/semantic_subtypes', methods=['GET'])
def semantics_identifier_semantic_subtypes_get(identifier):
    # Return information on semantic subtypes.
    return semantics_semantic_get(identifier, isforsubtypes=True)

def semantics_semantic_get(identifier, isforsubtypes:bool):
    """
    Returns a set of semantic types that either:
    1. match the identifier
    2. are subtypes (have a IS_STY relationship with) the specified semantic type
    identifier.

    Identifiers can be of two types:

    1. Name (e.g., "Anatomical Structure")
    2. Type Unique Identifier (TUI) (e.g., "T017")

    :param semantic_type_id: single identifier

    """
    neo4j_instance = current_app.neo4jConnectionHelper.instance()

    # Validate parameters.
    # Check for invalid parameter names.
    err = validate_query_parameter_names(parameter_name_list=['skip', 'limit'])
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
    semtype = identifier

    result = semantics_semantic_id_semantic_get_logic(neo4j_instance, semtype=semtype, skip=skip, limit=limit,
                                                           isforsubtypes=isforsubtypes)
    if result is None or result == []:
        # Empty result
        if isforsubtypes:
            errtype = "No subtypes of a Semantic Type matching the specified identifier"
        else:
            errtype = "No Semantic Types match the specified identifier"

        err = get_404_error_string(prompt_string=f"{errtype}",
                                       custom_request_path=f"'{identifier}'")
        return make_response(err, 404)

    # Wrap origin and path list in a dictionary that will become the JSON response.
    dict_result = {'semantic_types':result}
    return jsonify(dict_result)

