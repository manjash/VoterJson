import os
from pathlib import Path
from flask import Flask
from dotenv import load_dotenv
from voterjsonr.database import db





def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        load_dotenv()
        app.config.from_mapping(
            SECRET_KEY=os.environ['SECRET_KEY'],
            SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
        )
    else:
        # load the test config if passed in
        dotenv_path = Path(test_config)
        load_dotenv(dotenv_path=dotenv_path)
        # load_dotenv()

        app.config.from_mapping(
            SECRET_KEY=os.environ['TEST_SECRET_KEY'],
            # SECRET_KEY='test',
            # SQLALCHEMY_DATABASE_URI='postgresql://postgres:qwerty123@$test_db:5432/voterjson_db_test',
            SQLALCHEMY_DATABASE_URI=os.environ['TEST_DATABASE_URL'],
        )

    db.init_app(app)

    from . import api
    app.register_blueprint(api.bp)

    from . import models as _

    with app.app_context():
        db.create_all()

    return app
