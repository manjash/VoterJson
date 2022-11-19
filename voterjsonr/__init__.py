import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_PORT=5432,
        DB_HOST='localhost',
        DB_NAME='voterjson_db',
        DB_USERNAME='postgres',
        DB_PASSWORD='qwerty123',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db_pg
    db_pg.init_app(app)

    from . import api
    app.register_blueprint(api.bp)

    return app
