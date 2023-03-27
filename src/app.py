import logging
import os

from flask import Flask

from routes.assaytype.assaytype_controller import assaytype_blueprint
from routes.codes.codes_controller import codes_blueprint
from routes.concepts.concepts_controller import concepts_blueprint
from routes.datasets.datasets_controller import datasets_blueprint
from routes.semantics.semantics_controller import semantics_blueprint
from routes.terms.terms_controller import terms_blueprint
from routes.tui.tui_controller import tui_blueprint
from routes.valueset.valueset_controller import valueset_blueprint

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


@app.route('/', methods=['GET'])
def index():
    return "Hello! This is UBKG-API service :)"


def main():
    app.run(port=8080, host='0.0.0.0')


if __name__ == '__main__':
    main()
