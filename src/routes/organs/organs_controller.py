from neo4j_manager import get_neo4j_manager
from flask import Blueprint, jsonify, request, abort

organs_blueprint = Blueprint('organs', __name__, url_prefix='/organs')

neo4jManager = get_neo4j_manager()


@organs_blueprint.route('/', methods=['GET'])
def get_organs():
    sab = request.args.get('sab').upper()
    if sab not in ['SENNET', 'HUBMAP']:
        return jsonify(f'Invalid sab specified ({sab}) sab query parameter must be one of SENNET or HUBMAP'), 400
    return jsonify(neo4jManager.get_organs(sab))
