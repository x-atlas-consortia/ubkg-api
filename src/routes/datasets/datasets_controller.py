from flask import Blueprint, jsonify, current_app

datasets_blueprint = Blueprint('datasets', __name__, url_prefix='/datasets')


@datasets_blueprint.route('', methods=['GET'])
def dataset_get(application_context='HUBMAP', data_type=None, description=None, alt_name=None, primary=None, contains_pii=None,
                vis_only=None, vitessce_hint=None, dataset_provider=None):
    """Returns information on a set of HuBMAP or SenNet dataset types, with options to filter the list to those with specific property values. Filters are additive (i.e., boolean AND)


    :param application_context: Required filter to indicate application context.
    :type application_context: str
    :param data_type: Optional filter for data_type
    :type data_type: str
    :param description: Optional filter for display name. Use URL-encoding (space &#x3D; %20).
    :type description: str
    :param alt_name: Optional filter for a single element in the alt-names list--i.e., return datasets for which alt-names includes a value that matches the parameter. Although the field is named &#39;alt-names&#39;, the parameter uses &#39;alt_name&#39;. Use URL-encoding (space &#x3D; %20)
    :type alt_name: str
    :param primary: Optional filter to filter to primary (true) or derived (false) assay.
    :type primary: str
    :param contains_pii: Optional filter for whether the dataset contains Patient Identifying Information (PII). Although the field is named &#39;contains-pii&#39;, use &#39;contains_pii&#39; as an argument.
    :type contains_pii: str
    :param vis_only: Optional filter for whether datasets are visualization only (true). Although the field is named &#39;vis-only&#39;, use &#39;vis_only&#39; as an argument.
    :type vis_only: str
    :param vitessce_hint: Optional filter for a single element in the vitessce_hint list--i.e., return datasets for which vitessce_hints includes a value that matches the parameter. Although the field is named &#39;vitessce-hints&#39;, use &#39;vitessce_hint&#39; as an argument.
    :type vitessce_hint: str
    :param dataset_provider: Optional filter to identify the dataset provider - IEC (iec)  or external (lab)
    :type dataset_provider: str

    :rtype: Union[List[DatasetPropertyInfo], Tuple[List[DatasetPropertyInfo], int], Tuple[List[DatasetPropertyInfo], int, Dict[str, str]]
    """
    return jsonify(
        current_app.neo4jManager.dataset_get(application_context, data_type, description, alt_name, primary, contains_pii, vis_only,
                                 vitessce_hint, dataset_provider))
