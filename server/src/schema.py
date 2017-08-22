from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String

Base = declarative_base()
engine = create_engine('sqlite:///app.db', echo=True)


class Team(Base):
    __tablename__ = 'teams'
    name = Column(String, primary_key=True)
    score = Column(Integer)
    members = relationship("User", back_populates="team")

    def __repr__(self):
        return "<Team(name='{}', members={})>".format(self.name, self.members)


class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    name = Column(String)
    password = Column(String)
    score = Column(Integer)

    team = relationship("Team", back_populates="members")
    team_name = Column(String, ForeignKey('teams.name'))

    def __repr__(self):
        return "<User(username='{}', name='{}', score={}, team='{}')>".format(self.username, self.name, self.score, self.team_name)


class Challenge(Base):
    __tablename__ = 'challenges'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Integer)
    text = Column(String)
    submissions = relationship("Submission", back_populates="challenge")

    def __repr__(self):
        return "<Challenge(id={}, value={}, text='{}')>".format(self.id, self.value, self.text)


class Submission(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user = Column(String)
    text = Column(String)

    challenge = relationship("Challenge", back_populates="submissions")
    challenge_id = Column(String, ForeignKey('challenges.id'))

    def __repr__(self):
        return "<Submission(id={}, user='{}', text='{}', challenge={})>".format(self.id, self.user, self.text, self.challenge_id)


Base.metadata.create_all(engine)
