from flask import Blueprint, jsonify, current_app, request

assaytype_blueprint = Blueprint('assaytype', __name__, url_prefix='/assaytype')


@assaytype_blueprint.route('/<name>', methods=['GET'])
def assaytype_name_get(name, application_context='HUBMAP'):
    """Returns information on a set of HuBMAP or SenNet dataset types, with options to filter the list to those with specific property values. Filters are additive (i.e., boolean AND)


    :param name: AssayType name
    :type name: str
    :param application_context: Filter to indicate application context
    :type application_context: str

    :rtype: Union[AssayTypePropertyInfo, Tuple[AssayTypePropertyInfo, int], Tuple[AssayTypePropertyInfo, int, Dict[str, str]]
    """
    query_string_application_context = request.args.get('application_context')
    if query_string_application_context is not None:
        application_context = query_string_application_context
    return jsonify(current_app.neo4jManager.assaytype_name_get(name, application_context))
