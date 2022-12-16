import json
import pytest
from voterjsonr.db_pg import get_db

POLL_RESULTS = "SELECT count(pv.id) as num, pc.choice_name FROM poll_votes pv " \
    "JOIN poll_choices pc on pc.id = pv.choice_id and pc.poll_id = pv.poll_id " \
    "JOIN poll p on p.id = pv.poll_id " \
    "WHERE p.poll_name = (%s) " \
    "GROUP BY pc.choice_name"

CHECK_CHOICES_FOR_BIRDS_POLL = "SELECT poll_choices.choice_name as cn FROM poll_choices " \
                   "JOIN poll on poll.id = poll_choices.poll_id " \
                   "WHERE poll_name = 'birds'"

VOTES_POLLID_1_CHOICEID_1 = "SELECT count(id) as num from poll_votes " \
                         "WHERE poll_id = 1 and choice_id = 1"

COUNT_VOTES_POLLID_1 = "SELECT count(id) as num from poll_votes " \
           "WHERE poll_id = 1"

BIRDS_CHOICES = {"jay", "blackbird", "sparrow"}


def test_create_poll(client, app):
    """Testing poll creation"""

    response = client.post('/api/createPoll/',
                           json={"poll_name": "birds", "choices": list(BIRDS_CHOICES)})
    assert response.status_code == 200
    assert json.loads(response.data) == {'status': 'OK'}

    with app.app_context():
        with get_db().cursor() as cur:
            cur.execute(CHECK_CHOICES_FOR_BIRDS_POLL)
            assert cur.fetchone() is not None
            cur.execute(CHECK_CHOICES_FOR_BIRDS_POLL)
            choice_names = {cn[0] for cn in cur.fetchall()}
            assert choice_names == BIRDS_CHOICES


@pytest.mark.parametrize(('poll_name', 'choices', 'message'), (
    ('', '', b'Name of the poll is required'),
    (12, '', b'Name of the poll is required'),
    ('a', '', b'Choices for the poll in list format are required'),
    ('animals', ['test1', 'test2'], b'Key (poll_name)=(animals) already exists'),
))
def test_create_poll_validation(client, poll_name, choices, message):
    response = client.post('/api/createPoll/', json={"poll_name": poll_name, "choices": choices})
    assert message in response.data


def test_poll_vote(client, app):
    with app.app_context():
        with get_db().cursor() as cur:
            cur.execute(COUNT_VOTES_POLLID_1)
            num_of_pokemons = cur.fetchone()[0]
            cur.execute(VOTES_POLLID_1_CHOICEID_1)
            num_of_vote_1 = cur.fetchone()[0]

    response = client.post('/api/poll/', json={"poll_id": 1, "choice_id": 1})
    assert response.status_code == 200
    assert json.loads(response.data) == {'status': 'OK'}

    with app.app_context():
        with get_db().cursor() as cur:
            cur.execute(COUNT_VOTES_POLLID_1)
            assert cur.fetchone()[0] == num_of_pokemons + 1
            cur.execute(VOTES_POLLID_1_CHOICEID_1)
            assert cur.fetchone()[0] == num_of_vote_1 + 1


@pytest.mark.parametrize(('poll_id', 'choice_id', 'message'), (
    ('', '', b'poll_id is required'),
    (1, '', b'choice_id for the vote is required'),
    (99999, 2, b'Key (poll_id)=(99999) is not present in table \\"poll\\"'),
    (1, 99999, b'Key (choice_id)=(99999) is not present in table \\"poll_choices\\"'),
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
        with get_db().cursor() as cur:
            test_poll_name = 'animals'
            cur.execute(POLL_RESULTS, (test_poll_name,))
            res_data = cur.fetchall()
            dict_res = {'poll_name': test_poll_name, 'results': {}}
            for num, choice_name in res_data:
                dict_res["results"][choice_name] = num
            assert dict_res == benchmark


@pytest.mark.parametrize(('poll_id', 'message'), (
    ('', b'Invalid poll_id type'),
    (99999, b"Poll with id = 99999 doesn't exist"),
))
def test_poll_results_validation(client, poll_id, message):
    response = client.post('/api/getResult/', json={'poll_id': poll_id})
    assert message in response.data
