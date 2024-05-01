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

from common_routes.codes.codes_controller import codes_blueprint
from common_routes.concepts.concepts_controller import concepts_blueprint
from common_routes.terms.terms_controller import terms_blueprint
from common_routes.semantics.semantics_controller import semantics_blueprint
from common_routes.status.status_controller import status_blueprint
from common_routes.database.database_controller import database_blueprint
from common_routes.node_types.node_types_controller import node_types_blueprint
from common_routes.property_types.property_types_controller import property_types_blueprint
from common_routes.relationship_types.relationship_types_controller import relationship_types_blueprint
from common_routes.sabs.sabs_controller import sabs_blueprint

logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s', level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


class UbkgAPI:
    def __init__(self, config, package_base_dir):
        """
        If config is a string then it will be treated as a local file path from which to load a file, e.g.
        ubkg_app = UbkgAPI('./app.cfg', package_base_dir).app

        If config is a Flask.config then it will be used directly, e.g.
        config =  Flask(__name__,
                instance_path=path.join(path.abspath(path.dirname(__file__)), 'instance'),
                instance_relative_config=True)\
            .config.from_pyfile('app.cfg')

        The 'package_base_dir' is the base directory of the package (e.g., the directory in which
        the VERSION and BUILD files are located.
        """

        self.app = Flask(__name__,
                         instance_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance'),
                         instance_relative_config=True)

        self.app.package_base_dir = package_base_dir
        logger.info(f"package_base_dir: {package_base_dir}")

        self.app.register_blueprint(codes_blueprint)
        self.app.register_blueprint(concepts_blueprint)
        self.app.register_blueprint(semantics_blueprint)
        self.app.register_blueprint(status_blueprint)
        # self.app.register_blueprint(tui_blueprint)
        self.app.register_blueprint(terms_blueprint)
        self.app.register_blueprint(database_blueprint)
        self.app.register_blueprint(node_types_blueprint)
        self.app.register_blueprint(property_types_blueprint)
        self.app.register_blueprint(relationship_types_blueprint)
        self.app.register_blueprint(sabs_blueprint)

        self.app.neo4jConnectionHelper = None

        try:
            if Neo4jConnectionHelper.is_initialized():
                self.app.neo4jConnectionHelper = Neo4jConnectionHelper.instance()
                logger.info("Neo4jManager has already been initialized")
            else:
                if isinstance(config, str):
                    logger.info(f'Config provided from file: {config}')
                    self.app.config.from_pyfile(config)
                    self.app.neo4jConnectionHelper = \
                        Neo4jConnectionHelper.create(self.app.config['SERVER'],
                                                     self.app.config['USERNAME'],
                                                     self.app.config['PASSWORD'],
                                                     self.app.config['TIMEOUT'],
                                                     self.app.config['ROWLIMIT'],
                                                     self.app.config['PAYLOADLIMIT'])
                else:
                    logger.info('Using provided Flask config.')
                    # Set self based on passed in config parameters
                    for key, value in config.items():
                        setattr(self, key, value)
                    self.app.neo4jConnectionHelper = \
                        Neo4jConnectionHelper.create(self.SERVER,
                                                     self.USERNAME,
                                                     self.PASSWORD,
                                                     28,
                                                     1000,
                                                     9437184)
                    logger.info("Initialized Neo4jManager successfully for: {self.SERVER}")
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
        ubkg_app = UbkgAPI('./app.cfg', Path(__file__).absolute().parent.parent.parent).app
        ubkg_app.run(host='0.0.0.0', port="5002")
    except Exception as e:
        print("Error during starting debug server.")
        print(str(e))
        logger.error(e, exc_info=True)
        print("Error during startup check the log file for further information")
