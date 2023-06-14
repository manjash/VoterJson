from sqlalchemy import func, desc
from .models import Poll, PollVotes, PollChoices


class PollsService:
    """Methods to create polls, vote and get poll results"""
    def __init__(self, db):
        self.db = db

    def get_poll_results(self, poll_id: int):

        if not isinstance(poll_id, int):
            raise Exception('Invalid poll_id type')

        poll_result = self.db.session.execute(self.db.select(
                                                Poll.poll_name,
                                                PollChoices.choice_name,
                                                func.count(PollVotes.id).label('count')
                                               )
                                .select_from(PollVotes)
                                .join(PollChoices, PollChoices.id == PollVotes.choice_id)
                                .join(Poll, Poll.id == PollVotes.poll_id)
                                .where(Poll.id == poll_id)
                                .group_by(Poll.poll_name
                                          , PollChoices.choice_name
                                          )
                                .order_by(desc("count"))
                               ).all()
        self.db.session.commit()

        if not poll_result:
            raise Exception(f"Poll with id = {poll_id} doesn't exist")
        res = {'results': {}}
        for poll_name, choice_name, count in poll_result:
            res['poll_name'] = poll_name
            res['results'][choice_name] = count
        return res

    def make_poll_vote(self, poll_id: int, choice_id: int):
        if not isinstance(poll_id, int):
            raise Exception('poll_id is required')
        if not isinstance(choice_id, int):
            raise Exception('choice_id for the vote is required')

        self.db.session.add(PollVotes(poll_id=poll_id, choice_id=choice_id))
        self.db.session.commit()

    def create_poll(self, name: str, choices: list):
        if not isinstance(name, str) or name == '':
            raise Exception('Name of the poll is required')
        if not isinstance(choices, list) or choices == []:
            raise Exception('Choices for the poll in list format are required')

        new_poll = Poll(poll_name=name)
        new_choices = []
        for choice in choices:
            new_choices.append(PollChoices(choice_name=choice, poll=new_poll))
        self.db.session.add(new_poll)
        self.db.session.add_all(new_choices)
        self.db.session.commit()
