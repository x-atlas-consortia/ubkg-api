# August 2024
# The validate_application_context logic is specific to the HuBMAP/SenNet UBKG context. The functionality has been
# moved to the code base in the hs-ontology-api repository.

from flask import request, abort, jsonify


def validate_application_context():
    application_context = request.args.get('application_context')
    if application_context is None:
        return abort(jsonify(
            f'Invalid application_context ({application_context}) specified. Please pass one of SENNET or HUBMAP')), 400
    return application_context
