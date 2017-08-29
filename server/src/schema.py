from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String

Base = declarative_base()
engine = create_engine('sqlite:///app.db', echo=True)


class Team(Base):
    __tablename__ = 'teams'
    name = Column(String, primary_key=True)
    members = relationship("User", back_populates="team")

    @hybrid_property
    def submissions(self):
        return sum([user.submissions for user in self.members])

    @hybrid_property
    def score(self):
        unique_submissions = {submit.challenge.id: submit for submit in self.submissions if submit.state == "accepted"}
        unique_submissions = unique_submissions.values()
        return sum([submit.challenge.value for submit in unique_submissions])

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

    submissions = relationship("Submission", back_populates="user")

    def __repr__(self):
        return "<User(username='{}', name='{}', score={}, team='{}')>".format(self.username, self.name, self.score, self.team_name)


class Challenge(Base):
    __tablename__ = 'challenges'

    identifier = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Integer)
    text = Column(String)
    submissions = relationship("Submission", back_populates="challenge")

    def __repr__(self):
        return "<Challenge(id={}, value={}, text='{}')>".format(self.identifier, self.value, self.text)


class Submission(Base):
    __tablename__ = 'submissions'

    identifier = Column(Integer, autoincrement=True, primary_key=True)
    text = Column(String)

    user = relationship("User", back_populates="submissions")
    user_name = Column(String, ForeignKey('users.name'))

    challenge = relationship("Challenge", back_populates="submissions")
    challenge_id = Column(Integer, ForeignKey('challenges.identifier'))

    @hybrid_property
    def team(self):
        return self.user.team

    def __repr__(self):
        return "<Submission(id={}, user='{}', text='{}', challenge={}, team={})>".format(self.identifier, self.user_name, self.text, self.challenge_id, self.team.name)


Base.metadata.create_all(engine)
