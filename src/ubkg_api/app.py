import logging
import os
from pathlib import Path

from flask import Flask, jsonify

from ubkg_api.neo4j_manager import Neo4jManager
from ubkg_api.routes.assaytype.assaytype_controller import assaytype_blueprint
from ubkg_api.routes.codes.codes_controller import codes_blueprint
from ubkg_api.routes.concepts.concepts_controller import concepts_blueprint
from ubkg_api.routes.datasets.datasets_controller import datasets_blueprint
from ubkg_api.routes.organs.organs_controller import organs_blueprint
from ubkg_api.routes.semantics.semantics_controller import semantics_blueprint
from ubkg_api.routes.terms.terms_controller import terms_blueprint
from ubkg_api.routes.tui.tui_controller import tui_blueprint
from ubkg_api.routes.valueset.valueset_controller import valueset_blueprint

logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s', level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance'),
            instance_relative_config=True)
app.config.from_pyfile('app.cfg')

app.register_blueprint(assaytype_blueprint)
app.register_blueprint(codes_blueprint)
app.register_blueprint(concepts_blueprint)
app.register_blueprint(datasets_blueprint)
app.register_blueprint(semantics_blueprint)
app.register_blueprint(tui_blueprint)
app.register_blueprint(valueset_blueprint)
app.register_blueprint(terms_blueprint)
app.register_blueprint(organs_blueprint)

neo4j = None

try:
    if Neo4jManager.is_initialized():
        neo4j = Neo4jManager.instance()
        logger.info("Neo4jManager has already been initialized")
    else:
        neo4j = Neo4jManager.create(app.config['SERVER'], app.config['USERNAME'], app.config['PASSWORD'])
        logger.info("Initialized Neo4jManager successfully :)")
except Exception:
    logger.exception('Failed to initialize the Neo4jManager :(. Please check the instance/app.cfg are '
                     'correct')

app.neo4jManager = neo4j


@app.route('/', methods=['GET'])
def index():
    return "Hello! This is UBKG-API service :)"


@app.route('/status', methods=['GET'])
def status():
    status_data = {
        # Use strip() to remove leading and trailing spaces, newlines, and tabs
        'version': (Path(__file__).absolute().parent.parent / 'VERSION').read_text().strip(),
        'build': (Path(__file__).absolute().parent.parent / 'BUILD').read_text().strip(),
        'neo4j_connection': False
    }
    is_connected = app.neo4jManager.check_connection()
    if is_connected:
        status_data['neo4j_connection'] = True

    return jsonify(status_data)


def main():
    app.run(debug=True, port=8080, host='0.0.0.0')


if __name__ == '__main__':
    main()
