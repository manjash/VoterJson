from typing import Union
from flask import (
    Blueprint, request, jsonify, Response
)
from voterjsonr.db_pg import get_db

POLL_RESULTS = 'SELECT p.poll_name, pc.choice_name, count(distinct pv.id) num_choice ' \
               'FROM poll_votes pv' \
              ' JOIN poll_choices pc ON pc.id = pv.choice_id' \
              ' JOIN poll p ON p.id = pv.poll_id' \
              ' WHERE pv.poll_id = (%s)' \
              ' GROUP BY pc.choice_name, p.poll_name' \
              ' ORDER BY num_choice DESC'

POLL_VOTE = "INSERT INTO poll_votes (poll_id, choice_id) VALUES (%s, %s);"

POLL_ID_FROM_POLL_CHOICES = "SELECT id FROM poll_choices WHERE poll_id = (%s);"

SELECT_ID_FROM_POLL = "SELECT id FROM poll WHERE id = (%s);"

CREATE_CHOICE = "INSERT INTO poll_choices (choice_name, poll_id) VALUES (%s, %s);"

CREATE_POLL_QUERY = "INSERT INTO poll (poll_name) VALUES (%s) RETURNING id;"

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/createPoll/', methods=('POST',))
def create_poll() -> Union[Response, tuple[Response, int]]:
    """
    To create a poll, use POST method:

    Request:
    {
        "poll_name":
            poll_name,
        "choices":
            [choice_1, choice_2, ..]
    }

    :return:
    status 200 or error message
    """

    data = request.get_json(force=False, silent=False)
    name, choices = data['poll_name'], data['choices']

    error = validate_create_poll(choices, name)
    if error:
        return json_error(error)

    db = get_db()

    with db.cursor() as cur:
        try:
            cur.execute(CREATE_POLL_QUERY, (name,))
            poll_id = cur.fetchone()[0]
        except:
            return json_error(f"Poll {name} is already registered")

        choice_poll_id = tuple([(choice, poll_id) for choice in choices])

        cur.executemany(CREATE_CHOICE, choice_poll_id)
        db.commit()
    return jsonify({'status': 'OK'})


def json_error(error, status=400) -> tuple[Response, int]:
    """Conversion of a string error message into json"""
    return jsonify({'Error': error}), status


def validate_create_poll(choices: Union[set, list, tuple], name: str) -> str:
    """Copy for the error message when validating a poll creation"""

    if not name:
        return 'Name of the poll is required'
    if not choices:
        return 'Choices for the poll are required'


def is_valid_poll_id(db, poll_id: int) -> Response:
    """Checking whether a poll with chosen poll_id exists in DB"""
    with db.cursor() as cur:
        cur.execute(SELECT_ID_FROM_POLL, (poll_id,))
        return cur.fetchone()


@bp.route('/poll/', methods=('POST',))
def poll_vote() -> Union[Response, tuple[Response, int]]:
    """To vote for a poll, make a POST request with relevant poll_id and choice_id:
    {
        "poll_id": int,
        "choice_id": int
    }
    """
    data = request.get_json(force=False, silent=False)
    poll_id, choice_id = data['poll_id'], data['choice_id']
    db = get_db()

    error = validate_poll(choice_id, poll_id)
    if error:
        return json_error(error)

    is_poll_id_in_db = is_valid_poll_id(db, poll_id)
    with db.cursor() as cur:
        cur.execute(POLL_ID_FROM_POLL_CHOICES, (poll_id,))
        choice_ids = [choice[0] for choice in cur.fetchall()]

        if not is_poll_id_in_db:
            return json_error(f"Poll with id = {poll_id} doesn't exist")
        if choice_id in choice_ids:
            cur.execute(POLL_VOTE, (poll_id, choice_id))
            db.commit()
        else:
            error_message = f'The choice_id = {choice_id} is not an option of the poll_id = {poll_id}'
            return json_error(error_message)

    return jsonify({'status': 'OK'})


def validate_poll(choice_id: int, poll_id: int):
    """Copy for the error message when validating a poll voting"""

    if not poll_id:
        return 'poll_id is required'
    if not choice_id:
        return 'choice_id for the vote is required'


@bp.route('/getResult/', methods=('POST', ))
def poll_results() -> Union[Response, tuple[Response, int]]:
    """To get poll results by the poll_id, make a POST request:
    {
        "poll_id": int
    }
    """

    data = request.get_json()
    poll_id = data['poll_id']
    db = get_db()

    error = validate_poll_results(poll_id)
    if error:
        return json_error(error)

    if not is_valid_poll_id(db, poll_id):
        return json_error(f"Poll with id = {poll_id} doesn't exist")

    with db.cursor() as cur:
        cur.execute(POLL_RESULTS, (poll_id, ))
        poll_result = cur.fetchall()
        db.commit()

    res = dict()
    res['results'] = {}
    for poll_name, choice_name, num_choice in poll_result:
        res['poll_name'] = poll_name
        res['results'][choice_name] = num_choice
    return jsonify(res)


def validate_poll_results(poll_id: int):
    """Copy for the error message when validating a request for poll results"""
    if not poll_id:
        return 'poll_id is required'
