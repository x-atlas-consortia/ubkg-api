from flask import Blueprint, jsonify, current_app, request, make_response

from routes.validate import validate_application_context

assayname_blueprint = Blueprint('assayname', __name__, url_prefix='/assayname')


@assayname_blueprint.route('', methods=['POST'])
def assayname_post():
    """Get the assaytypes with name and alt-names as found in the request body with key 'name'.
    This is a replacement for search-src endpoint of the same name.

    :param application_context: Filter to indicate application context
    :type application_context: str

    :rtype: Union[AssayTypePropertyInfo, Tuple[AssayTypePropertyInfo, int], Tuple[AssayTypePropertyInfo, int, Dict[str, str]]
    """
    application_context = validate_application_context()
    if not request.is_json:
        return make_response("A JSON body with a 'Content-Type: application/json' header are required", 400)
    if 'name' not in request.json:
        return make_response('Request contains no "name" field', 400)
    req_name = request.json['name']
    if type(req_name) == list:
        name = req_name[0]
        alt_names = req_name[1:]
    elif type(req_name) == str:
        name = req_name
        alt_names = None
    result = current_app.neo4jManager.assaytype_name_get(name, alt_names, application_context)
    if result is None:
        return make_response(f"No such assay_type {req_name}, even as alternate name", 400)
    return jsonify(result)
