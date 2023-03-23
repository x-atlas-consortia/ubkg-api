from flask import Blueprint, jsonify

from api.managers.neo4j_manager import Neo4jManager

assaytype_blueprint = Blueprint('assaytype', __name__, url_prefix='/assaytype')
neo4jManager = Neo4jManager()


@assaytype_blueprint.route('/<name>', methods=['GET'])
def assaytype_name_get(name, application_context=None):  # noqa: E501
    """Returns information on a set of HuBMAP or SenNet dataset types, with options to filter the list to those with specific property values. Filters are additive (i.e., boolean AND)

     # noqa: E501

    :param name: AssayType name
    :type name: str
    :param application_context: Filter to indicate application context
    :type application_context: str

    :rtype: Union[AssayTypePropertyInfo, Tuple[AssayTypePropertyInfo, int], Tuple[AssayTypePropertyInfo, int, Dict[str, str]]
    """
    return jsonify(neo4jManager.assaytype_name_get(name, application_context))
