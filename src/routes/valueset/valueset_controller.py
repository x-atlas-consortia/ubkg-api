from flask import Blueprint, jsonify, current_app

valueset_blueprint = Blueprint('valueset', __name__, url_prefix='/valueset')


@valueset_blueprint.route('/', methods=['GET'])
def valueset_get(parent_sab, parent_code, child_sabs):
    """Returns a valueset of concepts that are children (have as isa relationship) of another concept.


    :param parent_sab: the SAB of the parent concept
    :type parent_sab: str
    :param parent_code: the code of the parent concept in the SAB (local ontology)
    :type parent_code: str
    :param child_sabs: the list of SABs for child concepts, in order of preference (in case of parent concepts with cross-references)
    :type child_sabs: List[str]

    :rtype: Union[List[SabCodeTerm], Tuple[List[SabCodeTerm], int], Tuple[List[SabCodeTerm], int, Dict[str, str]]
    """
    return jsonify(current_app.neo4jManager.valueset_get(parent_sab, parent_code, child_sabs))