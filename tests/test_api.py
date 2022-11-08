import pytest
from voterjsonr.db import get_db
import json

POLL_RESULTS = "SELECT count(pv.id) as num, pc.choice_name FROM poll_votes pv " \
    "JOIN poll_choices pc on pc.id = pv.choice_id and pc.poll_id = pv.poll_id " \
    "JOIN poll p on p.id = pv.poll_id " \
    "WHERE p.poll_name = (?) " \
    "GROUP BY pc.choice_name"

CHECK_CHOICES_FOR_BIRDS_POLL = "SELECT poll_choices.choice_name as cn FROM poll_choices " \
                   "JOIN poll on poll.id = poll_choices.poll_id " \
                   "WHERE poll_name = 'birds'"

COUNT_VOTES_POLLID_1_CHOICEID_1 = "SELECT count(id) as num from poll_votes " \
                         "WHERE poll_id = 1 and choice_id = 1"

COUNT_VOTES_POLLID_1 = "SELECT count(id) as num from poll_votes " \
           "WHERE poll_id = 1"

BIRDS_CHOICES = {"jay", "blackbird", "sparrow"}


def test_create_poll(client, app):
    response = client.post('/api/createPoll/', json={"poll_name": "birds", "choices": list(BIRDS_CHOICES)})
    assert response.status_code == 200
    assert json.loads(response.data) == {'status': 'OK'}

    with app.app_context() as app:
        assert get_db().execute(CHECK_CHOICES_FOR_BIRDS_POLL).fetchone() is not None # count instead or just skip
        choice_names = get_db().execute(CHECK_CHOICES_FOR_BIRDS_POLL).fetchall()
        choice_names = set([cn['cn'] for cn in choice_names])
        assert choice_names == BIRDS_CHOICES


@pytest.mark.parametrize(('poll_name', 'choices', 'message'), (
    ('', '', b'Name of the poll is required'),
    ('a', '', b'Choices for the poll are required'),
    ('pokemons', 'test', b'Poll pokemons is already registered'),
))
def test_create_poll_validation(client, poll_name, choices, message):
    response = client.post('/api/createPoll/', json={"poll_name": poll_name, "choices": choices})
    assert message in response.data


def test_poll_vote(client, app):
    with app.app_context():
        num_of_pokemons = get_db().execute(COUNT_VOTES_POLLID_1).fetchone()['num']
        num_of_vote_1 = get_db().execute(COUNT_VOTES_POLLID_1_CHOICEID_1).fetchone()['num']

    response = client.post('/api/poll/', json={"poll_id": 1, "choice_id": 1})
    assert response.status_code == 200
    assert json.loads(response.data) == {'status': 'OK'}

    with app.app_context():
        assert get_db().execute(COUNT_VOTES_POLLID_1).fetchone()['num'] == num_of_pokemons + 1
        assert get_db().execute(COUNT_VOTES_POLLID_1_CHOICEID_1).fetchone()['num'] == num_of_vote_1 + 1


@pytest.mark.parametrize(('poll_id', 'choice_id', 'message'), (
    ('', '', b'poll_id is required'),
    (1, '', b'choice_id for the vote is required'),
    (99999, 2, b"Poll with id = 99999 doesn't exist"),
    (1, 99999, b"The choice_id = 99999 is not an option of the poll_id = 1"),
))
def test_poll_vote_validation(client, poll_id, choice_id, message):
    response = client.post('/api/poll/', json={'poll_id': poll_id, 'choice_id': choice_id})
    assert message in response.data


def test_poll_results(client, app):

    response = client.post('/api/getResult/', json={"poll_id": 2})
    assert response.status_code == 200

    benchmark = {"poll_name": "animals", "results": {"cat": 4, "dog": 2, "parrot": 4, "hamster": 5}}
    assert benchmark == json.loads(response.data)

    with app.app_context():
        test_poll_name = 'animals'
        res_data = get_db().execute(POLL_RESULTS, (test_poll_name,)).fetchall()
        dict_res = {'poll_name': test_poll_name, 'results': dict()}
        for num, choice_name in res_data:
            dict_res["results"][choice_name] = num
        assert dict_res == benchmark


@pytest.mark.parametrize(('poll_id', 'message'), (
    ('', b'poll_id is required'),
    (99999, b"Poll with id = 99999 doesn't exist"),
))
def test_poll_results_validation(client, poll_id, message):
    response = client.post('/api/getResult/', json={'poll_id': poll_id})
    assert message in response.data
