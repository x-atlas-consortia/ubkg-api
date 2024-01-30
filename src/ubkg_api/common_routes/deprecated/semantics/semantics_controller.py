# JAS January 2024
# Deprecated. SUIs currently only apply to Concepts managed by the UMLS.
from flask import Blueprint, jsonify, current_app
from src.ubkg_api.common_routes.common_neo4j_logic import semantics_semantic_id_semantics_get_logic

semantics_blueprint = Blueprint('semantics', __name__, url_prefix='/semantics')


@semantics_blueprint.route('/<semantic_id>/semantics', methods=['GET'])
def semantics_semantic_id_semantics_get(semantic_id):
    """Returns a list of semantic_types {queryTUI, querySTN ,semantic, TUI_STN} of the semantic type

    :param semantic_id: The semantic identifier
    :type semantic_id: str

    :rtype: Union[List[QQST], Tuple[List[QQST], int], Tuple[List[QQST], int, Dict[str, str]]
    """
    neo4j_instance = current_app.neo4jConnectionHelper.instance()
    return jsonify(semantics_semantic_id_semantics_get_logic(neo4j_instance, semantic_id))
