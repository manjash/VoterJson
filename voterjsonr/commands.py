import click
import json
from flask import Flask, request, g, current_app
from voterjsonr.db import get_db
from voterjsonr import app

# app = Flask(__name__)
# app = current_app

# {"name": 'Poll', "choices": ['1', '2', '3', '4']}


# @app.route('/api/createPoll/', methods=('GET', 'POST'))
def create_poll(): # ???? need typehint
    if request.method == 'GET':
        return 'Create a poll'
    if request.method == 'POST':
        data = request.get_json(force=False, silent=False)
        name, choices = data['name'], data['choices']
        db = get_db()
        error = None

        if not name:
            error = 'Name of the poll is required'
            return error
        elif not choices:
            error = 'Choices for the poll are required'
            return error

        if error is None:
            try:
                poll_id = db.execute(
                    "INSERT INTO poll (poll_name) VALUES (?) RETURNING id",
                    (name,)
                ).fetchone()['id']
                print()
                print(poll_id)
            except db.IntegrityError:
                error = f"Poll {name} is already registered"
                return error

            # query_str = "INSERT INTO poll_choices (choice_name, poll_id) VALUES %s;" % ', '.join(['(?, ?)' for i in range(len(choices))])
            for choice in choices:
                db.execute(
                    "INSERT INTO poll_choices (choice_name, poll_id) VALUES (?, ?);",
                    (choice, poll_id)
                )
            db.commit()
            return 'Poll created'


app.add_url_rule('/api/createPoll/', view_func=create_poll)


def is_valid_poll_id(db, poll_id: int): #???? Need typehint for DB
    return db.execute("SELECT id FROM poll WHERE id = (?)", (poll_id, )).fetchone()

@app.route('/api/poll/', methods=('POST', 'GET'))
def poll_vote():  # ????? need typehint?
    if request.method == 'GET':
        return 'Make your choice'
    if request.method == 'POST':
        data = request.get_json(force=False, silent=False)
        poll_id, choice_id = data['poll_id'], data['choice_id']
        db = get_db()
        error = None

        if not poll_id:
            error = 'poll_id is required'
            return error
        elif not choice_id:
            error = 'choice_id for the vote is required'
            return error

        if error is None:
            is_poll_id_in_db = is_valid_poll_id(db, poll_id)
            choice_ids_for_the_poll = [choice['id'] for choice in db.execute(
                "SELECT id FROM poll_choices WHERE poll_id = (?)",
                (poll_id,)
            ).fetchall()]

            if not is_poll_id_in_db:
                return f"Poll with id = {poll_id} doesn't exist"
            elif choice_id in choice_ids_for_the_poll:
                print('in the if')
                db.execute(
                    "INSERT INTO poll_votes (poll_id, choice_id) VALUES (?, ?)",
                    (poll_id, choice_id)
                )
            else:
                return f'The choice_id = {choice_id} is not an option of the poll_id = {poll_id}'
            db.commit()
            return 'Your vote is accepted'



@app.route('/api/getResult/', methods=('POST', 'GET'))
def poll_results() -> dict:
    if request.method == 'GET':
        return 'Get poll results'
    if request.method == 'POST':
        data = request.get_json()
        poll_id = data['poll_id']
        db = get_db()
        error = None

        if not is_valid_poll_id(db, poll_id):
            return f"Poll with id = {poll_id} doesn't exist"
        else:
            poll_result = db.execute(
                'select p.poll_name, pc.choice_name, count(distinct pv.id) num_choice from poll_votes pv'
                ' join poll_choices pc on pc.id = pv.choice_id'
                ' join poll p on p.id = pv.poll_id'
                ' where pv.poll_id = (?)'
                ' group by pc.choice_name'
                ' order by count(distinct pv.id) desc',
                (poll_id, )
                        ).fetchall()
            db.commit()

            res = dict()
            res['results'] = []
            for poll_name, choice_name, num_choice in poll_result:
                print()
                res['poll_name'] = poll_name
                res['results'].append((choice_name, num_choice))
        return res
