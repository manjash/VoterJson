from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from voterjsonr.database import db

# pylint: disable=too-few-public-methods,missing-class-docstring
class Poll(db.Model):
    __tablename__ = 'poll'

    id = Column(Integer, primary_key=True)
    poll_name = Column(String(256), unique=True, nullable=False)
    poll_choices = relationship("PollChoices", backref="poll")


# pylint: disable=too-few-public-methods,missing-class-docstring
class PollChoices(db.Model):
    __tablename__ = 'poll_choices'
    id = Column(Integer, primary_key=True)
    choice_name = Column(String(128), nullable=False)
    poll_id = Column(Integer, ForeignKey('poll.id'), nullable=False)


# pylint: disable=too-few-public-methods,missing-class-docstring
class PollVotes(db.Model):
    __tablename__ = 'poll_votes'
    id = Column(Integer, primary_key=True)
    poll_id = Column(Integer, ForeignKey('poll.id'), nullable=False)
    choice_id = Column(Integer, ForeignKey('poll_choices.id'), nullable=False)
