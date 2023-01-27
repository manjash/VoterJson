import os
from flask import Flask
from dotenv import load_dotenv
from voterjsonr.database import db

load_dotenv()





def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ['SECRET_KEY'],
            DB_PORT=int(os.environ['DB_PORT']),
            DB_HOST=os.environ['DB_HOST'],
            DB_NAME=os.environ['DB_NAME'],
            DB_USERNAME=os.environ['DB_USERNAME'],
            DB_PASSWORD=os.environ['DB_PASSWORD'],
            SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
        )
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    db.init_app(app)

    from . import models as _

    with app.app_context():
        db.create_all()

    from . import api
    app.register_blueprint(api.bp)

    return app
