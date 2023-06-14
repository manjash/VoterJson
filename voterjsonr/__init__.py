import os
from flask import Flask
from voterjsonr.database import db


def create_app(test_config=None):  # pylint: disable=W0613
    # create and configure the app
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.environ['SECRET_KEY'],
        SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
    )

    db.init_app(app)

    from . import api
    app.register_blueprint(api.bp)

    from . import models as _

    with app.app_context():
        db.create_all()

    return app
