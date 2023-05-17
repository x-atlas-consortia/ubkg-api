import logging
import os
from pathlib import Path

from flask import Flask, jsonify

from neo4j_manager import Neo4jManager
from routes.assaytype.assaytype_controller import assaytype_blueprint
from routes.codes.codes_controller import codes_blueprint
from routes.concepts.concepts_controller import concepts_blueprint
from routes.datasets.datasets_controller import datasets_blueprint
from routes.organs.organs_controller import organs_blueprint
from routes.semantics.semantics_controller import semantics_blueprint
from routes.terms.terms_controller import terms_blueprint
from routes.tui.tui_controller import tui_blueprint
from routes.valueset.valueset_controller import valueset_blueprint

logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s', level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


class UbkgAPI:
    def __init__(self, config):

        self.app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance'), instance_relative_config=True)

        self.app.register_blueprint(assaytype_blueprint)
        self.app.register_blueprint(codes_blueprint)
        self.app.register_blueprint(concepts_blueprint)
        self.app.register_blueprint(datasets_blueprint)
        self.app.register_blueprint(semantics_blueprint)
        self.app.register_blueprint(tui_blueprint)
        self.app.register_blueprint(valueset_blueprint)
        self.app.register_blueprint(terms_blueprint)
        self.app.register_blueprint(organs_blueprint)

        neo4j = None

        try:
            if Neo4jManager.is_initialized():
                neo4j = Neo4jManager.instance()
                logger.info("Neo4jManager has already been initialized")
            else:
                if not config:
                    logger.info('Config not provided. Looking for app.cfg ...')
                    self.app.config.from_pyfile('app.cfg')
                    neo4j = Neo4jManager.create(self.app.config['SERVER'], self.app.config['USERNAME'], self.app.config['PASSWORD'])
                else:
                    logger.info('Using provided config.')
                    # Set self based on passed in config parameters
                    for key, value in config.items():
                        setattr(self, key, value)
                    neo4j = Neo4jManager.create(self.SERVER, self.USERNAME, self.PASSWORD)
                logger.info("Initialized Neo4jManager successfully :)")
        except Exception:
            logger.exception('Failed to initialize the Neo4jManager :(. Please check that the provided config dictionary is correct or the instance/app.cfg is '
                             'correct')

        self.app.neo4jManager = neo4j

        @self.app.route('/', methods=['GET'])
        def index():
            return "Hello! This is UBKG-API service :)"

        @self.app.route('/status', methods=['GET'])
        def status():
            status_data = {
                # Use strip() to remove leading and trailing spaces, newlines, and tabs
                'version': (Path(__file__).absolute().parent.parent / 'VERSION').read_text().strip(),
                'build': (Path(__file__).absolute().parent.parent / 'BUILD').read_text().strip(),
                'neo4j_connection': False
            }
            is_connected = self.app.neo4jManager.check_connection()
            if is_connected:
                status_data['neo4j_connection'] = True

            return jsonify(status_data)


####################################################################################################
## For local development/testing
####################################################################################################

if __name__ == "__main__":
    flask_app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance'),
            instance_relative_config=True)
    flask_app.config.from_pyfile('app.cfg')

    try:
        ubkg_app = UbkgAPI(flask_app.config).app
        ubkg_app.run(host='0.0.0.0', port="5002")
    except Exception as e:
        print("Error during starting debug server.")
        print(str(e))
        logger.error(e, exc_info=True)
        print("Error during startup check the log file for further information")
