import os
import tempfile
import psycopg2
import subprocess
from urllib.parse import urlparse

import pytest
from voterjsonr import create_app
from voterjsonr.db_pg import get_db, init_db, close_db, drop_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


# def pg_tmp():
#     pg_tmp_result = subprocess.check_output(
#         ['pg_tmp', '-t'],
#         encoding="utf-8",
#         env={**os.environ,
#              # 'PATH': '/Library/PostgreSQL/15/bin:/Users/manjash/local/bin/:' + os.environ['PATH']}
#              'PATH': '/Library/PostgreSQL/15/bin:/Users/manjash/local/bin/:' + os.environ['PATH']}
#     ).strip()
#     url = urlparse(pg_tmp_result)
#     port = url.port
#     host = url.hostname
#     dbname = url.path.lstrip('/')
#     username = url.username
#     return port, host, dbname, username

@pytest.fixture
def app():
    # port, host, dbname, username = pg_tmp()

    app = create_app(
    #     {
    #     'TESTING': True,
    #     'DB_PORT': port,
    #     'DB_HOST': host,
    #     'DB_NAME': dbname,
    #     'DB_USERNAME': username,
    # }
    )

    ## For pg_tmp
    # app.config.from_mapping(
    #     SECRET_KEY='test',
    #     DB_PORT=port,
    #     DB_HOST=host,
    #     DB_NAME=dbname,
    #     DB_USERNAME=username,
    #     # DB_PASSWORD='qwerty123',
    # )

    # From Eugene
    app.config.from_mapping(
        SECRET_KEY=os.environ['TEST_SECRET_KEY'],
        DB_PORT=int(os.environ['TEST_DB_PORT']),
        DB_HOST=os.environ['TEST_DB_HOST'],
        DB_NAME=os.environ['TEST_DB_NAME'],
        DB_USERNAME=os.environ['TEST_DB_USERNAME'],
        DB_PASSWORD=os.environ['TEST_DB_PASSWORD'],
    )

    with app.app_context():
        drop_db()
        init_db()
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute(_data_sql)
        conn.commit()
    yield app

    # close_db()




@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

