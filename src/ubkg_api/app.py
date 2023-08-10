import os
import sys
import logging
from pathlib import Path
from flask import Flask

# To fix the ModuleNotFoundError when used as a package
path_root = Path(__file__).parents[0]
sys.path.append(str(path_root))

# Local modules
from neo4j_connection_helper import Neo4jConnectionHelper

from common_routes.assaytype.assaytype_controller import assaytype_blueprint
from common_routes.assayname.assayname_controller import assayname_blueprint
from common_routes.codes.codes_controller import codes_blueprint
from common_routes.concepts.concepts_controller import concepts_blueprint
from common_routes.semantics.semantics_controller import semantics_blueprint
from common_routes.terms.terms_controller import terms_blueprint
from common_routes.tui.tui_controller import tui_blueprint

logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s', level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


class UbkgAPI:
    def __init__(self, config_file):
        """
        Create a flask app using the config_file provided. Attach the blueprints to the app, as well as an
        instance to the Neo4JConnectionHelper.
        """
        self.app = Flask(__name__,
                         instance_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance'),
                         instance_relative_config=True)

        if not self.app.config.from_pyfile(config_file):
            logger.error(f'Failed to load config file: {config_file}')
            raise ValueError(f'Failed to load config file: {config_file}')
        self.app.register_blueprint(assaytype_blueprint)
        self.app.register_blueprint(assayname_blueprint)
        self.app.register_blueprint(codes_blueprint)
        self.app.register_blueprint(concepts_blueprint)
        self.app.register_blueprint(semantics_blueprint)
        self.app.register_blueprint(tui_blueprint)
        self.app.register_blueprint(terms_blueprint)

        self.app.neo4jConnectionHelper = None

        if Neo4jConnectionHelper.is_initialized():
            self.app.neo4jConnectionHelper = Neo4jConnectionHelper.instance()
            logger.info("Neo4jManager has already been initialized")
        else:
            try:
                self.app.neo4jConnectionHelper = \
                    Neo4jConnectionHelper.create(self.app.config['SERVER'],
                                                 self.app.config['USERNAME'],
                                                 self.app.config['PASSWORD'])
                logger.info("Initialized Neo4jManager successfully")
            except Exception as e:
                logger.exception('Failed to initialize the Neo4jManager')
                raise e

        @self.app.route('/', methods=['GET'])
        def index():
            return "Hello! This is UBKG-API service :)"


####################################################################################################
## For local development/testing
####################################################################################################

if __name__ == "__main__":
    try:
        ubkg_app = UbkgAPI('./app.cfg').app
        ubkg_app.run(host='0.0.0.0', port="5002")
    except Exception as e:
        print("Error during starting debug server.")
        print(str(e))
        logger.error(e, exc_info=True)
        print("Error during startup check the log file for further information")
