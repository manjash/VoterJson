import os
import pytest
from voterjsonr import create_app
from voterjsonr import db
from sqlalchemy.sql import text

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    flask_app = create_app()
    flask_app.config.from_mapping(
        SECRET_KEY=os.environ['TEST_SECRET_KEY'],
        DB_PORT=int(os.environ['TEST_DB_PORT']),
        DB_HOST=os.environ['TEST_DB_HOST'],
        DB_NAME=os.environ['TEST_DB_NAME'],
        DB_USERNAME=os.environ['TEST_DB_USERNAME'],
        DB_PASSWORD=os.environ['TEST_DB_PASSWORD'],
        SQLALCHEMY_DATABASE_URI=os.environ['TEST_DATABASE_URL'],
    )

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
