from flask import request, abort, jsonify


def validate_application_context():
    application_context = request.args.get('application_context')
    if application_context is None:
        return abort(jsonify(
            f'Invalid application_context ({application_context}) specified. Please pass one of SENNET or HUBMAP')), 400
    return application_context
