from flask import Blueprint, jsonify, current_app, request, abort, make_response

from routes.validate import validate_application_context

assayname_blueprint = Blueprint('assayname', __name__, url_prefix='/assayname')


@assayname_blueprint.route('', methods=['POST'])
def assayname_post():
    """Get all of the assaytypes with name.
    This is a replacement for search-src endpoint of the same name.

    :param name: AssayType name
    :type name: str
    :param application_context: Filter to indicate application context
    :type application_context: str

    :rtype: Union[AssayTypePropertyInfo, Tuple[AssayTypePropertyInfo, int], Tuple[AssayTypePropertyInfo, int, Dict[str, str]]
    """
    application_context = validate_application_context()
    if not request.is_json:
        abort(400, "A JSON body with a 'Content-Type: application/json' header are required")
    if 'name' not in request.json:
        abort(400, 'request contains no "name" field')
    name = request.json['name']
    if type(name) == list:
        name = name[0]
    return jsonify(current_app.neo4jManager.assaytype_name_get(name, application_context))