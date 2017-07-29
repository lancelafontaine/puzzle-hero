from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    password = Column(String)
    score = Column(Integer)
    team = Column(String)

    def __repr__(self):
        return "<User(name='{}', fullname='{}', password='{}')>".format(self.username, self.name, self.password)


# class Team(Base):
#     __tablename__ = 'teams'
#     name = Column(String, primary_key=True)
#     members = relationship(User)


engine = create_engine('sqlite:///app.db', echo=True)

Base.metadata.create_all(engine)
