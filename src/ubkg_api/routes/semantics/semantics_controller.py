from flask import Blueprint, jsonify, current_app

semantics_blueprint = Blueprint('semantics', __name__, url_prefix='/semantics')


@semantics_blueprint.route('/<semantic_id>/semantics', methods=['GET'])
def semantics_semantic_id_semantics_get(semantic_id):
    """Returns a list of semantic_types {queryTUI, querySTN ,semantic, TUI_STN} of the semantic type


    :param semantic_id: The semantic identifier
    :type semantic_id: str

    :rtype: Union[List[QQST], Tuple[List[QQST], int], Tuple[List[QQST], int, Dict[str, str]]
    """
    return jsonify(current_app.neo4jManager.semantics_semantic_id_semantics_get(semantic_id))
