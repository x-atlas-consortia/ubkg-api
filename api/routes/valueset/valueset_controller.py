from flask import Blueprint, jsonify

from api.managers.neo4j_manager import Neo4jManager

valueset_blueprint = Blueprint('valueset', __name__, url_prefix='/valueset')
neo4jManager = Neo4jManager()


@valueset_blueprint.route('/', methods=['GET'])
def valueset_get(parent_sab, parent_code, child_sabs):  # noqa: E501
    """Returns a valueset of concepts that are children (have as isa relationship) of another concept.

     # noqa: E501

    :param parent_sab: the SAB of the parent concept
    :type parent_sab: str
    :param parent_code: the code of the parent concept in the SAB (local ontology)
    :type parent_code: str
    :param child_sabs: the list of SABs for child concepts, in order of preference (in case of parent concepts with cross-references)
    :type child_sabs: List[str]

    :rtype: Union[List[SabCodeTerm], Tuple[List[SabCodeTerm], int], Tuple[List[SabCodeTerm], int, Dict[str, str]]
    """
    return jsonify(neo4jManager.valueset_get(parent_sab, parent_code, child_sabs))