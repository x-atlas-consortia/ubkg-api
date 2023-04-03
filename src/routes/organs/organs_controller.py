from flask import Blueprint, jsonify, request, current_app

organs_blueprint = Blueprint('organs', __name__, url_prefix='/organs')


@organs_blueprint.route('', methods=['GET'])
def get_organ_types():
    application_context = request.args.get('application_context').upper()
    if application_context not in ['SENNET', 'HUBMAP']:
        return jsonify(f'Invalid application_context specified ({application_context}) application_context query '
                       f'string must be one of SENNET or HUBMAP'), 400
    return jsonify(current_app.neo4jManager.get_organ_types(application_context))
