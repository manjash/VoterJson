from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# pylint: disable=too-few-public-methods,missing-class-docstring
class Poll(Base):
    __tablename__ = 'poll'

    id = Column(Integer, primary_key=True)
    poll_name = Column(String(256), unique=True, nullable=False)
    poll_choices = relationship("PollChoices", backref="poll")

# pylint: disable=too-few-public-methods,missing-class-docstring
class PollChoices(Base):
    __tablename__ = 'poll_choices'
    id = Column(Integer, primary_key=True)
    choice_name = Column(String(128), nullable=False)
    poll_id = Column(Integer, ForeignKey('poll.id'), nullable=False)

# pylint: disable=too-few-public-methods,missing-class-docstring
class PollVotes(Base):
    __tablename__ = 'poll_votes'
    id = Column(Integer, primary_key=True)
    poll_id = Column(Integer, ForeignKey('poll.id'), nullable=False)
    choice_id = Column(Integer, ForeignKey('poll_choices.id'), nullable=False)
