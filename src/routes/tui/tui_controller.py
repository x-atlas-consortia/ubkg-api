from flask import Blueprint, jsonify, current_app

tui_blueprint = Blueprint('tui', __name__, url_prefix='/tui')


@tui_blueprint.route('<tui_id>/semantics', methods=['GET'])
def tui_tui_id_semantics_get(tui_id):
    """Returns a list of symantic_types {semantic, STN} of the type unique id (tui)


    :param tui_id: The TUI identifier
    :type tui_id: str

    :rtype: Union[List[SemanticStn], Tuple[List[SemanticStn], int], Tuple[List[SemanticStn], int, Dict[str, str]]
    """
    return jsonify(current_app.neo4jManager.tui_tui_id_semantics_get(tui_id))