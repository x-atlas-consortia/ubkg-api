from neo4j_manager import get_neo4j_manager
from flask import Blueprint, jsonify, request

organs_blueprint = Blueprint('organs', __name__, url_prefix='/organs')

neo4jManager = get_neo4j_manager()


@organs_blueprint.route('/', methods=['GET'])
def get_organs():
    sab = request.args.get('sab')
    return jsonify(neo4jManager.get_organs(sab))
