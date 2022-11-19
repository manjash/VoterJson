import psycopg2
import pytest
from voterjsonr.db_pg import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(psycopg2.InterfaceError) as e:
        with db.cursor() as cur:
            cur.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    # What is this for??? What does this test ???
    monkeypatch.setattr('voterjsonr.db_pg.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
