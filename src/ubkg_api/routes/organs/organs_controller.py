from flask import Blueprint, jsonify, request, current_app

organs_blueprint = Blueprint('organs', __name__, url_prefix='/organs')


@organs_blueprint.route('', methods=['GET'])
def get_organ_types():
    application_context = 'HUBMAP'
    query_string = request.args.get('application_context')
    if query_string is not None:
        application_context = query_string.upper()
    if application_context not in ['SENNET', 'HUBMAP']:
        return jsonify(f'Invalid application_context specified ({application_context}) application_context query '
                       f'string must be one of SENNET or HUBMAP'), 400
    return jsonify(current_app.neo4jManager.get_organ_types(application_context))

@organs_blueprint.route('by-code', methods=['GET'])
def get_organ_by_code():
    application_context = 'HUBMAP'
    query_string = request.args.get('application_context')
    if query_string is not None:
        application_context = query_string.upper()
    if application_context not in ['SENNET', 'HUBMAP']:
        return jsonify(f'Invalid application_context specified ({application_context}) application_context query '
                       f'string must be one of SENNET or HUBMAP'), 400
    data: list = current_app.neo4jManager.get_organ_types(application_context)
    result: dict = {}
    for item in data:
        result[item['rui_code']] = item['term'].strip()
    return jsonify(result)
