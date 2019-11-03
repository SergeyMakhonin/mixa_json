import os
from logging_and_configuration import log
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_json('config.json', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        log('Instance path {path} does not exist.'.format(path=app.instance_path))

    # client main page
    @app.route('/client_main/<path:sub_path>', methods=['GET'])
    def client_main(sub_path):
        return ''

    # register auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    return app