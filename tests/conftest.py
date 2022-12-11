import os
import pytest
from voterjsonr import create_app
from voterjsonr.db_pg import get_db, init_db, drop_db

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
    )

    with flask_app.app_context():
        drop_db()
        init_db()
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute(_data_sql)
        conn.commit()
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
