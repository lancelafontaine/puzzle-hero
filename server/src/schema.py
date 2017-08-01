from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String

Base = declarative_base()
engine = create_engine('sqlite:///app.db', echo=True)


class Team(Base):
    __tablename__ = 'teams'
    name = Column(String, primary_key=True)
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
    __tablename__ = 'Challenges'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Integer)
    text = Column(String)

    def __repr__(self):
        return "<Challenge(id={}, value={}, text='{}')>".format(self.id, self.value, self.text)


Base.metadata.create_all(engine)
