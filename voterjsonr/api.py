
from typing import Union
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, Response
)
from werkzeug.security import check_password_hash, generate_password_hash
from voterjsonr.db import get_db

POLL_RESULTS = 'SELECT p.poll_name, pc.choice_name, count(distinct pv.id) num_choice FROM poll_votes pv' \
                      ' JOIN poll_choices pc ON pc.id = pv.choice_id' \
                      ' JOIN poll p ON p.id = pv.poll_id' \
                      ' WHERE pv.poll_id = (?)' \
                      ' GROUP BY pc.choice_name' \
                      ' ORDER BY count(distinct pv.id) DESC'

POLL_VOTE = "INSERT INTO poll_votes (poll_id, choice_id) VALUES (?, ?)"

POLL_ID_FROM_POLL_CHOICES = "SELECT id FROM poll_choices WHERE poll_id = (?)"

SELECT_ID_FROM_POLL = "SELECT id FROM poll WHERE id = (?)"

CREATE_CHOICE = "INSERT INTO poll_choices (choice_name, poll_id) VALUES (?, ?);"

CREATE_POLL_QUERY = "INSERT INTO poll (poll_name) VALUES (?) RETURNING id"

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/createPoll/', methods=('POST',))
def create_poll() -> Union[Response, tuple[Response, int]]:
    data = request.get_json(force=False, silent=False)
    name, choices = data['poll_name'], data['choices']

    error = validate_create_poll(choices, name)
    if error:
        return json_error(error)

    db = get_db()

    try:
        poll_id = db.execute(CREATE_POLL_QUERY, (name,)).fetchone()['id']
    except db.IntegrityError:
        return json_error(f"Poll {name} is already registered")

    choice_poll_id = tuple([(choice, poll_id) for choice in choices])

    db.executemany(CREATE_CHOICE, choice_poll_id)
    db.commit()
    return jsonify({'status': 'OK'})


def json_error(error, status=400) -> tuple[Response, int]:
    return jsonify({'Error': error}), status


def validate_create_poll(choices: Union[set, list, tuple], name: str) -> str:
    if not name:
        return 'Name of the poll is required'
    elif not choices:
        return 'Choices for the poll are required'


def is_valid_poll_id(db, poll_id: int) -> Response:
    return db.execute(SELECT_ID_FROM_POLL, (poll_id,)).fetchone()


@bp.route('/poll/', methods=('POST',))
def poll_vote() -> Union[Response, tuple[Response, int]]:
    data = request.get_json(force=False, silent=False)
    poll_id, choice_id = data['poll_id'], data['choice_id']
    db = get_db()

    error = validate_poll(choice_id, poll_id)
    if error:
        return json_error(error)

    is_poll_id_in_db = is_valid_poll_id(db, poll_id)
    choice_ids = [choice['id'] for choice in db.execute(POLL_ID_FROM_POLL_CHOICES, (poll_id,)).fetchall()]

    if not is_poll_id_in_db:
        return json_error(f"Poll with id = {poll_id} doesn't exist")
    elif choice_id in choice_ids:
        db.execute(POLL_VOTE, (poll_id, choice_id))
        db.commit()
    else:
        return json_error(f'The choice_id = {choice_id} is not an option of the poll_id = {poll_id}')

    return jsonify({'status': 'OK'})


def validate_poll(choice_id: int, poll_id: int):
    if not poll_id:
        return 'poll_id is required'
    elif not choice_id:
        return 'choice_id for the vote is required'


@bp.route('/getResult/', methods=('POST', ))
def poll_results() -> Union[Response, tuple[Response, int]]:
    data = request.get_json()
    poll_id = data['poll_id']
    db = get_db()

    error = validate_poll_results(poll_id)
    if error:
        return json_error(error)

    if not is_valid_poll_id(db, poll_id):
        return json_error(f"Poll with id = {poll_id} doesn't exist")

    poll_result = db.execute(POLL_RESULTS, (poll_id, )).fetchall()
    db.commit()

    res = dict()
    res['results'] = dict()
    for poll_name, choice_name, num_choice in poll_result:
        res['poll_name'] = poll_name
        res['results'][choice_name] = num_choice
    return jsonify(res)


def validate_poll_results(poll_id: int):
    if not poll_id:
        return 'poll_id is required'
