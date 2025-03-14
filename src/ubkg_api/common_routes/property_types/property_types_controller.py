from flask import Blueprint, jsonify, current_app, make_response, request
from ..common_neo4j_logic import property_types_get_logic
from utils.http_error_string import get_404_error_string, validate_query_parameter_names, \
    validate_parameter_value_in_enum, validate_required_parameters, validate_parameter_is_numeric, \
    validate_parameter_is_nonnegative, validate_parameter_range_order, check_payload_size
from utils.http_parameter import parameter_as_list, set_default_minimum, set_default_maximum

# S3 redirect functions
from utils.s3_redirect import redirect_if_large

property_types_blueprint = Blueprint('property-types', __name__, url_prefix='/property-types')


@property_types_blueprint.route('', methods=['GET'])
def property_type_get():
    # Returns property types
    neo4j_instance = current_app.neo4jConnectionHelper.instance()

    result = property_types_get_logic(neo4j_instance)
    if result is None or result == []:
        err = get_404_error_string(prompt_string="No property keys", timeout = neo4j_instance.timeout)
        return make_response(err, 404)

    # Mar 2025
    return redirect_if_large(resp=result)
