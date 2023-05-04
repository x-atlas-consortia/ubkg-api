from flask import Blueprint, jsonify, request, current_app, abort

organs_blueprint = Blueprint('organs', __name__, url_prefix='/organs')


@organs_blueprint.route('', methods=['GET'])
def get_organ_types():
    application_context = request.args.get('application_context')
    validate_application_context_query_string_parameter(application_context)
    return jsonify(current_app.neo4jManager.get_organ_types(application_context.upper()))


@organs_blueprint.route('by-code', methods=['GET'])
def get_organ_by_code():
    application_context = request.args.get('application_context')
    validate_application_context_query_string_parameter(application_context)
    data: list = current_app.neo4jManager.get_organ_types(application_context.upper())
    result: dict = {}
    for item in data:
        result[item['rui_code']] = item['term'].strip()
    return jsonify(result)


def validate_application_context_query_string_parameter(application_context):
    if application_context is None:
        return abort(jsonify(f'Invalid application_context specified ({application_context}) application_context query '
                             f'string must be one of SENNET or HUBMAP')), 400
