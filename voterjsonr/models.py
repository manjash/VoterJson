from voterjsonr import db


class Poll(db.Model):
    __tablename__ = 'poll'

    id = db.Column(db.Integer, primary_key=True)
    poll_name = db.Column(db.String(256), unique=True, nullable=False)
    poll_choices = db.relationship("PollChoices", backref="poll")

    def __init__(self, poll_name):
        self.poll_name = poll_name

    def __repr__(self):
        return f'<Poll {self.poll_name}>'


class PollChoices(db.Model):
    __tablename__ = 'poll_choices'
    id = db.Column(db.Integer, primary_key=True)
    choice_name = db.Column(db.String(128), nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)

# ------> if uncomment this - error in pylint in poll_services.py 58:31

    # def __init__(self, choice_name):
    #     self.choice_name = choice_name
    #
    # def __repr__(self):
    #     return f'<PollChoices {self.choice_name}>'


class PollVotes(db.Model):
    __tablename__ = 'poll_votes'
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    choice_id = db.Column(db.Integer, db.ForeignKey('poll_choices.id'), nullable=False)

    # def __init__(self, choice_id, poll_id):
    #     self.choice_id = choice_id
    #     self.poll_id = poll_id
    #
    # def __repr__(self):
    #     return f'<PollVotes {self.poll_id}>'
