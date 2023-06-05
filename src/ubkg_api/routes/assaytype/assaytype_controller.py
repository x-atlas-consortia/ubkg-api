from flask import Blueprint, jsonify, current_app, request

from routes.validate import validate_application_context

assaytype_blueprint = Blueprint('assaytype', __name__, url_prefix='/assaytype')


@assaytype_blueprint.route('', methods=['GET'])
def assaytype_get():
    """
    Get all of the assaytypes without query parameter.
    ?primary=true Only get those where record['primary'] == True
    ?primary=false Only get those where record['primary'] == False

    :return:
    """
    primary: bool = request.args.get('primary', default=None)
    if primary is not None:
        primary = primary.lower() == 'true'
    application_context = validate_application_context()
    return jsonify(current_app.neo4jManager.assaytype_get(primary, application_context))


@assaytype_blueprint.route('/<name>', methods=['GET'])
def assaytype_name_get(name):
    """Get all of the assaytypes with name.
    This is a replacement for search-src endpoint of the same name.

    :param name: AssayType name
    :type name: str
    :param application_context: Filter to indicate application context
    :type application_context: str

    :rtype: Union[AssayTypePropertyInfo, Tuple[AssayTypePropertyInfo, int], Tuple[AssayTypePropertyInfo, int, Dict[str, str]]
    """
    application_context = validate_application_context()
    return jsonify(current_app.neo4jManager.assaytype_name_get(name, application_context))
