from config import config
import requests
from schema import User


def slack_users():
    token_data = {'token': config['slackToken']}
    return requests.get(config['slackApiUrl'] + '/users.list', params=token_data)


def app_users(session):
    return session.query(User).all()


# probably works? have not tested
def validate_user(session, data):
    user = session.query(User).filter(User.username == username).one()
    return password == user.password


# not even slightly functional
def team_users(session, team_name):
    users = session.query(User).filter(User.team == team_name)


def add_user(session, data):
    user = User(username=data['username'], name=data['name'], password=data['password'], score=0)
    try:
        session.add(user)
        session.commit()
        return True, "Successfully added User {}".format(data["username"])
    except e:
        return False, e.message


def join_team(session, username, team):
    pass
