from flask import Blueprint, jsonify, current_app, make_response, request
from ..common_neo4j_logic import relationship_types_get_logic
from utils.http_error_string import get_404_error_string, validate_query_parameter_names, \
    validate_parameter_value_in_enum, validate_required_parameters, validate_parameter_is_numeric, \
    validate_parameter_is_nonnegative, validate_parameter_range_order, check_payload_size
from utils.http_parameter import parameter_as_list, set_default_minimum, set_default_maximum

relationship_types_blueprint = Blueprint('relationship-types', __name__, url_prefix='/relationship-types')


@relationship_types_blueprint.route('', methods=['GET'])
def relationship_type_get():
    # Returns relationship types
    neo4j_instance = current_app.neo4jConnectionHelper.instance()

    result = relationship_types_get_logic(neo4j_instance)
    if result is None or result == []:
        err = get_404_error_string(prompt_string="No relationship types")
        return make_response(err, 404)

    return jsonify(result)
