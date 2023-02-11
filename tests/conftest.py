import os
import pytest
from sqlalchemy.sql import text
from voterjsonr import create_app
from voterjsonr.database import db


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    flask_app = create_app(test_config=".env.testing")

    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        db.session.execute(text(_data_sql))
        db.session.commit()
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
