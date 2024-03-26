from flask import Blueprint, jsonify, current_app

status_blueprint = Blueprint('status', __name__, url_prefix='/status')


"""
Show the status of the Neo4j connection, the current VERSION and BUILD.

Returns
-------
json
    A json containing the status details
"""
@status_blueprint.route('', methods = ['GET'])
def get_status():

    try:
        file_version_content = (current_app.package_base_dir / 'VERSION').read_text().strip()
    except Exception as e:
        file_version_content = str(e)

    try:
        file_build_content = (current_app.package_base_dir / 'BUILD').read_text().strip()
    except Exception as e:
        file_build_content = str(e)

    neo4j_instance = current_app.neo4jConnectionHelper.instance()
    status_data = {
        'version': file_version_content,
        'build': file_build_content,
        'neo4j_connection': neo4j_instance.check_connection()
    }

    return jsonify(status_data)
