from flask import Blueprint, jsonify, current_app, make_response, request
from ..common_neo4j_logic import sab_code_count_get, sab_code_detail_get, sab_term_type_get_logic,\
    sabs_get_logic
from utils.http_error_string import get_404_error_string, validate_query_parameter_names, \
    validate_parameter_value_in_enum, validate_required_parameters, validate_parameter_is_numeric, \
    validate_parameter_is_nonnegative, validate_parameter_range_order, check_payload_size
from utils.http_parameter import parameter_as_list, set_default_minimum, set_default_maximum

sabs_blueprint = Blueprint('sabs', __name__, url_prefix='/sabs')

@sabs_blueprint.route('', methods=['GET'])
def sabs_get():
    # Return list of SABS.
    neo4j_instance = current_app.neo4jConnectionHelper.instance()

    return sabs_get_logic(neo4j_instance)

@sabs_blueprint.route('/codes/counts', methods=['GET'])
def sabs_codes_counts_get():
    # Return SABs and counts of codes for all SABs.
    return sabs_codes_counts_get()

@sabs_blueprint.route('<sab>/codes/counts', methods=['GET'])
def sabs_codes_counts_sab_get(sab):
    # Return SAB and count of codes for specified SAB.
    return sabs_codes_counts_get(sab)


def sabs_codes_counts_get(sab=None):
    # Returns relationship types
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

    result = sab_code_count_get(neo4j_instance, sab=sab, skip=skip, limit=limit)
    iserr = result is None or result == []
    if not iserr:
        # Check for empty sab data, which may happen in response either to invalid SAB or a skip > number of records.
        sabscheck = result.get('sabs')
        iserr = len(sabscheck) == 0
        if not iserr:
            sabcheck = sabscheck[0].get('sab')
            iserr = sabcheck is None

    if iserr:
        err = get_404_error_string(prompt_string="No sources",
                                   custom_request_path=f"sab='{sab}'")
        return make_response(err, 404)

    return jsonify(result)


@sabs_blueprint.route('/codes/details', methods=['GET'])
def sabs_codes_details_get():
    """
    The underlying query that returns code details cannot be run for all sabs on large UBKG instances.
    """

    err = f'The response to this endpoint cannot be run for all SABs because of memory limitations. ' \
          f'Execute the /sabs/codes/details/(sab) endpoint with the identifier for a SAB. Execute ' \
          f'the /sabs endpoint for a list of all SABs in the UBKG.'
    return make_response(err, 400)


@sabs_blueprint.route('<sab>/codes/details', methods=['GET'])
def sabs_codes_details_sab_get(sab):

    # Returns details on codes associated with the specified SAB.

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

    result = sab_code_detail_get(neo4j_instance, sab=sab, skip=skip, limit=limit)
    iserr = False
    if result is None or result == []:
        iserr = True
    else:
        # Check for empty code data, which may happen in response either to invalid SAB or a skip > number of records.
        codes = result.get('codes')
        iserr = len(codes) == 0
        if not iserr:
            code = codes[0].get('code')
            iserr = code is None

    if iserr:
        err = get_404_error_string(prompt_string="No codes",
                                   custom_request_path=f"sab='{sab}'", timeout=neo4j_instance.timeout)
        return make_response(err, 404)

    return jsonify(result)


@sabs_blueprint.route('term-types', methods=['GET'])
def sabs_term_types_get():
    """
        The underlying query that returns term types cannot be run for all sabs on large UBKG instances.
        """

    err = f'The response to this endpoint cannot be run for all SABs because of memory limitations. ' \
          f'Execute the /sabs/term-types/(sab) endpoint with the identifier for a SAB. Execute ' \
          f'the /sabs endpoint for a list of all SABs in the UBKG.'
    return make_response(err, 400)


@sabs_blueprint.route('<sab>/term-types', methods=['GET'])
def sabs_sab_term_types_get(sab):

    # Returns term types for the SAB.

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

    result = sab_term_type_get_logic(neo4j_instance, sab=sab, skip=skip, limit=limit)

    iserr = result is None or result == []
    if not iserr:
        # Check for empty subtype data.
        if type(result) == list:
            termtypes = result[0].get('term_types')
        else:
            termtypes = result.get('term_types')
        iserr = len(termtypes) == 0

    if iserr:
        err = get_404_error_string(prompt_string="No term types", custom_request_path=f"sab='{sab}'")
        return make_response(err, 404)

    return jsonify(result)
