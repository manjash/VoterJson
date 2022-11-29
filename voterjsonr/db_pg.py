import psycopg2

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
                host=current_app.config['DB_HOST'],
                database=current_app.config['DB_NAME'],
                user=current_app.config['DB_USERNAME'],
                password=current_app.config['DB_PASSWORD'],
                port=current_app.config['DB_PORT'],
        )

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with db.cursor() as cur:
        with current_app.open_resource('schema.sql') as f:
            cur.execute(f.read().decode('utf8'))
            db.commit()


def drop_db():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("drop schema public cascade;"
                    "create schema public;"
                    "grant all on schema public to postgres;"
                    "grant all on schema public to public;")
        db.commit()



@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


