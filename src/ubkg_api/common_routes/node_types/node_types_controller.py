from flask import Blueprint, jsonify, current_app, make_response, request
from ..common_neo4j_logic import node_types_node_type_counts_by_sab_get_logic, \
    node_types_node_type_counts_get_logic, node_types_get_logic
from utils.http_error_string import get_404_error_string, validate_query_parameter_names, \
    validate_parameter_value_in_enum, validate_required_parameters, validate_parameter_is_numeric, \
    validate_parameter_is_nonnegative, validate_parameter_range_order, check_payload_size
from utils.http_parameter import parameter_as_list, set_default_minimum, set_default_maximum

node_types_blueprint = Blueprint('node-types', __name__, url_prefix='/node-types')


@node_types_blueprint.route('', methods=['GET'])
def node_type_get():
    # Return list of node types.
    neo4j_instance = current_app.neo4jConnectionHelper.instance()
    return node_types_get_logic(neo4j_instance)

@node_types_blueprint.route('counts', methods=['GET'])
def node_type_counts_get():

    # Return counts of all node_types.
    # return node_types_counts_get()

    """
        Although it is possible to obtain counts for all node types, the query response time for large
        databases (such as the Data Distillery) is likely to exceed the API server timeout.

        Instead of allowing the execution of an endpoint that is likely to result in timeouts,
        require the specification of a node type.

        If the configured timeout can be increased to above 40 s, then this route could call
        node_types_counts_get with node_type=None.
        """

    neo4j_instance = current_app.neo4jConnectionHelper.instance()
    err = f'The response to this endpoint is likely to exceed the timeout ' \
          f'of {int(neo4j_instance.timeout / 1000)} seconds and so will not be attempted. ' \
          f'Execute the node_types/(node_type) endpoint ' \
          f'with the name of a node type (e.g., Codes). To obtain names of node types, execute the ' \
          f'node_types endpoint.'
    return make_response(err, 400)


@node_types_blueprint.route('<node_type>/counts', methods=['GET'])
def node_type_counts_node_type_get(node_type):
    # Return counts of a specific node type.
    return node_types_counts_get(node_type)


def node_types_counts_get(node_type=None):
    """
    Returns information on a set of node types.
    :param node_type: node_type for filtering.

    """
    neo4j_instance = current_app.neo4jConnectionHelper.instance()

    result = node_types_node_type_counts_get_logic(neo4j_instance, node_type=node_type)
    iserr = result is None or result == []
    if not iserr:
        # Check for empty node_type data.
        if type(result) == list:
            total_count = result[0].get('total_count')
        else:
            total_count = result.get('total_count')
        iserr = total_count == 0

    if iserr:
        errtype = "No Node Types"

        err = get_404_error_string(prompt_string=f"{errtype}",
                                   custom_request_path=f"node_type='{node_type}'",
                                   timeout=neo4j_instance.timeout)
        return make_response(err, 404)

    return jsonify(result)


@node_types_blueprint.route('counts-by-sab', methods=['GET'])
def node_types_counts_by_sab_get():
    """
    Although it is possible to obtain counts for all node types by SAB, the query response time for large
    databases (such as the Data Distillery) is likely to exceed the API server timeout. (Running the query
    against an instance of Data Distillery requires around 36 s on a MacBook Pro with 64 GB RAM.)

    Instead of
    allowing the execution of an endpoint that is likely to result in timeouts, require the specification of
    a node type.

    If the configured timeout can be increased to above 40 s, then this route can call
    node_types_counts_by_sab_node_type_get with node_type=None.
    """

    neo4j_instance = current_app.neo4jConnectionHelper.instance()
    err = f'The response to this endpoint is likely to exceed the timeout ' \
          f'of {int(neo4j_instance.timeout/1000)} seconds and so will not be attempted. ' \
          f'Execute the node_types/counts_by_sab/(node_type) endpoint ' \
          f'with the name of a node type (e.g., Codes) and SAB. To obtain names of node types, execute the ' \
          f'node_types endpoint.'
    return make_response(err, 400)


@node_types_blueprint.route('<node_type>/counts-by-sab', methods=['GET'])
def node_types_counts_by_sab_node_type_get(node_type):
    """
    Returns information on a set of node types, grouped by SAB

    :param node_type: node_type for filtering.

    """
    neo4j_instance = current_app.neo4jConnectionHelper.instance()

    # Validate parameters.
    # Check for invalid parameter names.
    err = validate_query_parameter_names(parameter_name_list=['sab'])
    if err != 'ok':
        return make_response(err, 400)

    # Check for required parameters.
    # Note: the sab is a required parameter only because the endpoint /node_types/counts_by_sab has been
    # blocked. If it should be possible to run the endpoint without specifying a sab, this validation
    # can be removed.
    err = validate_required_parameters(required_parameter_list=['sab'])
    if err != 'ok':
        return make_response(err, 400)

    # Get remaining parameter values from the path or query string.
    sab = parameter_as_list(param_name='sab')

    result = node_types_node_type_counts_by_sab_get_logic(neo4j_instance, node_type=node_type, sab=sab)
    iserr = False
    if result is None or result == []:
        iserr = True
    else:
        # Check for empty node_type data.
        if type(result) == list:
            total_count = result[0].get('total_count')
        else:
            total_count = result.get('total_count')
        iserr = total_count == 0

    if iserr:
        errtype = "No Node Types"

        err = get_404_error_string(prompt_string=f"{errtype}",
                                   custom_request_path=f"node_type='{node_type}'",
                                   timeout=neo4j_instance.timeout)
        return make_response(err, 404)

    return jsonify(result)
