from typing import Union
from flask import (
    Blueprint, request, jsonify, Response
)
from voterjsonr.polls_service import PollsService
from voterjsonr.database import db

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

    service = PollsService(db)

    try:
        service.create_poll(name, choices)
    except Exception as err:
        return json_error(err.args[0])
    return jsonify({'status': 'OK'})


def json_error(error, status=400) -> tuple[Response, int]:
    """Conversion of a string error message into json"""
    return jsonify({'Error': error}), status


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

    service = PollsService(db)
    try:
        service.make_poll_vote(poll_id, choice_id)
    except Exception as err:
        return json_error(err.args[0])
    return jsonify({'status': 'OK'})
#
#
@bp.route('/getResult/', methods=('POST', ))
def poll_results() -> Union[Response, tuple[Response, int]]:
    """To get poll results by the poll_id, make a POST request:
    {
        "poll_id": int
    }
    """

    data = request.get_json()
    poll_id = data['poll_id']

    service = PollsService(db)
    try:
        res = service.get_poll_results(poll_id)
    except Exception as err:
        return json_error(err.args[0])
    return jsonify(res)
