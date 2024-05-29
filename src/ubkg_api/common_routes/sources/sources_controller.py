from flask import Blueprint, jsonify, current_app, make_response, request
from ..common_neo4j_logic import sources_get_logic
from utils.http_error_string import get_404_error_string, validate_query_parameter_names, \
    validate_parameter_value_in_enum, validate_required_parameters, validate_parameter_is_numeric, \
    validate_parameter_is_nonnegative, validate_parameter_range_order, check_payload_size
from utils.http_parameter import parameter_as_list, set_default_minimum, set_default_maximum

sources_blueprint = Blueprint('sources', __name__, url_prefix='/sources')


@sources_blueprint.route('', methods=['GET'])
def sources_get():

    # Returns relationship types

    neo4j_instance = current_app.neo4jConnectionHelper.instance()

    # Validate parameters.
    # Check for invalid parameter names.
    err = validate_query_parameter_names(parameter_name_list=['sab', 'context'])
    if err != 'ok':
        return make_response(err, 400)

    sab = parameter_as_list(param_name='sab')
    context = parameter_as_list(param_name='context')
    # JAS 24 May 2024
    # Validate context parameter against enum.
    val_enum = ['base_context', 'data_distillery_context', 'hubmap_sennet_context']
    if context is not None:
        for c in context:
            c = c.lower()
            err = validate_parameter_value_in_enum(param_name='context', param_value=c,
                                               enum_list=val_enum)
        if err != 'ok':
            return make_response(err, 400)

    result = sources_get_logic(neo4j_instance, sab=sab, context=context)
    iserr = result is None or result == []

    if not iserr:
        # Check for no results.
        sources = result.get('sources')
        iserr = len(sources) == 0

    if iserr:
        err = get_404_error_string(prompt_string="No sources")
        return make_response(err, 404)

    return jsonify(result)
