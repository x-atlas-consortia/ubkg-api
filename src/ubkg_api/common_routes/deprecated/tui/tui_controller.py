# JAS January 2024
# Deprecated. SUIs currently only apply to Concepts managed by the UMLS.
from flask import Blueprint, jsonify, current_app
from src.ubkg_api.common_routes.common_neo4j_logic import tui_tui_id_semantics_get_logic

tui_blueprint = Blueprint('tui', __name__, url_prefix='/tui')


@tui_blueprint.route('<tui_id>/semantics', methods=['GET'])
def tui_tui_id_semantics_get(tui_id):
    """Returns a list of symantic_types {semantic, STN} of the type unique id (tui)

    :param tui_id: The TUI identifier
    :type tui_id: str

    :rtype: Union[List[SemanticStn], Tuple[List[SemanticStn], int], Tuple[List[SemanticStn], int, Dict[str, str]]
    """
    neo4j_instance = current_app.neo4jConnectionHelper.instance()
    return jsonify(tui_tui_id_semantics_get_logic(neo4j_instance, tui_id))
