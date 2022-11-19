import os
import tempfile
import psycopg2
import subprocess
from urllib.parse import urlparse

import pytest
from voterjsonr import create_app
from voterjsonr.db_pg import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


def pg_tmp():
    pg_tmp_result = subprocess.check_output(
        ['pg_tmp', '-t'],
        encoding="utf-8",
        env={**os.environ,
             'PATH': '/Library/PostgreSQL/15/bin:/Users/manjash/local/bin/:' + os.environ['PATH']}
    ).strip()
    url = urlparse(pg_tmp_result)
    port = url.port
    host = url.hostname
    dbname = url.path.lstrip('/')
    username = url.username
    return port, host, dbname, username

@pytest.fixture
def app():
    port, host, dbname, username = pg_tmp()

    app = create_app({
        'TESTING': True,
        'DB_PORT': port,
        'DB_HOST': host,
        'DB_NAME': dbname,
        'DB_USERNAME': username,
    })

    with app.app_context():
        init_db()
        with get_db().cursor() as cur:
            cur.execute(_data_sql)
            # for testing
            cur.execute('select poll_name from poll;')
            print('---##----->', cur.fetchall())

    yield app



@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

