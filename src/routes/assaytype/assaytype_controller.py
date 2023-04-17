from flask import Blueprint, jsonify, current_app, request

assaytype_blueprint = Blueprint('assaytype', __name__, url_prefix='/assaytype')


@assaytype_blueprint.route('', methods=['GET'])
def assaytype_get(application_context='HUBMAP'):
    """
    Get all of the assaytypes without query parameter.
    ?primary=true Only get those where record['primary'] == True
    ?primary=false Only get those where record['primary'] == False

    :param application_context:
    :return:
    """
    primary: bool = request.args.get('primary', default=None)
    if primary is not None:
        primary = primary.lower() == 'true'
    query_string_application_context = request.args.get('application_context')
    if query_string_application_context is not None:
        application_context = query_string_application_context
    return jsonify(current_app.neo4jManager.assaytype_get(primary, application_context))

@assaytype_blueprint.route('/<name>', methods=['GET'])
def assaytype_name_get(name, application_context='HUBMAP'):
    """Get all of the assaytypes with name.

    :param name: AssayType name
    :type name: str
    :param application_context: Filter to indicate application context
    :type application_context: str

    :rtype: Union[AssayTypePropertyInfo, Tuple[AssayTypePropertyInfo, int], Tuple[AssayTypePropertyInfo, int, Dict[str, str]]
    """
    if application_context not in ['SENNET', 'HUBMAP']:
        return jsonify(f'Invalid application_context specified ({application_context}) application_context query '
                       f'string must be one of SENNET or HUBMAP'), 400
    return jsonify(current_app.neo4jManager.assaytype_name_get(name, application_context))
