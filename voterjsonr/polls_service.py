from voterjsonr.db_pg import get_db

POLL_RESULTS = 'SELECT p.poll_name, pc.choice_name, count(distinct pv.id) num_choice ' \
               'FROM poll_votes pv' \
              ' JOIN poll_choices pc ON pc.id = pv.choice_id' \
              ' JOIN poll p ON p.id = pv.poll_id' \
              ' WHERE pv.poll_id = (%s)' \
              ' GROUP BY pc.choice_name, p.poll_name' \
              ' ORDER BY num_choice DESC'

POLL_ID_FROM_POLL_CHOICES = "SELECT id FROM poll_choices WHERE poll_id = (%s);"

POLL_VOTE = "INSERT INTO poll_votes (poll_id, choice_id) VALUES (%s, %s);"

CREATE_POLL_QUERY = "INSERT INTO poll (poll_name) VALUES (%s) RETURNING id;"

CREATE_CHOICE = "INSERT INTO poll_choices (choice_name, poll_id) VALUES (%s, %s);"


class PollsService():
    """Methods to create polls, vote and get poll results"""
    def __init__(self):
        self.db = get_db()

    def get_poll_results(self, poll_id: int):

        if not isinstance(poll_id, int):
            raise Exception('Invalid poll_id type')

        with self.db.cursor() as cur:
            cur.execute(POLL_RESULTS, (poll_id,))
            poll_result = cur.fetchall()
            self.db.commit()

        if not poll_result:
            raise Exception(f"Poll with id = {poll_id} doesn't exist")
        
        res = {'results': {}}
        for poll_name, choice_name, num_choice in poll_result:
            res['poll_name'] = poll_name
            res['results'][choice_name] = num_choice
        return res

    def make_poll_vote(self, poll_id: int, choice_id: int):
        if not isinstance(poll_id, int):
            raise Exception('poll_id is required')
        if not isinstance(choice_id, int):
            raise Exception('choice_id for the vote is required')

        with self.db.cursor() as cur:
            cur.execute(POLL_VOTE, (poll_id, choice_id))
            self.db.commit()

    def create_poll(self, name: str, choices: list):
        if not isinstance(name, str) or name == '':
            raise Exception('Name of the poll is required')
        if not isinstance(choices, list) or choices == []:
            raise Exception('Choices for the poll in list format are required')

        with self.db.cursor() as cur:
            cur.execute(CREATE_POLL_QUERY, (name,))
            poll_id = cur.fetchone()[0]
            choice_poll_id = ([(choice, poll_id) for choice in choices])
            cur.executemany(CREATE_CHOICE, choice_poll_id)
            self.db.commit()
