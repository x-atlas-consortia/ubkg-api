from flask import Blueprint, jsonify

from api.managers.neo4j_manager import Neo4jManager

tui_blueprint = Blueprint('tui', __name__, url_prefix='/tui')
neo4jManager = Neo4jManager()


@tui_blueprint.route('<tui_id>/semantics', methods=['GET'])
def tui_tui_id_semantics_get(tui_id):  # noqa: E501
    """Returns a list of symantic_types {semantic, STN} of the type unique id (tui)

     # noqa: E501

    :param tui_id: The TUI identifier
    :type tui_id: str

    :rtype: Union[List[SemanticStn], Tuple[List[SemanticStn], int], Tuple[List[SemanticStn], int, Dict[str, str]]
    """
    return jsonify(neo4jManager.tui_tui_id_semantics_get(tui_id))