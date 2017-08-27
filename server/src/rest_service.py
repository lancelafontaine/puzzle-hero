from config import config
import requests
from schema import User, Team


def slack_users():
    token_data = {'token': config['slackToken']}
    return requests.get(config['slackApiUrl'] + '/users.list', params=token_data)


def app_users(db_session, filters):
    return db_session.query(User).filter_by(**filters)


def teams(db_session, filters):
    return db_session.query(Team).filter_by(**filters)


def authenticate_user(db_session, data):
    user = db_session.query(User).filter(User.username == data['username']).one()
    result = data['password'] == user.password
    message = "Successfully authenticated user {}" if result else "Failed to authenticate user {}"
    return result, message.format(data["username"])


def add_user(db_session, data):
    user = User(username=data['username'], name=data['name'], password=data['password'], score=0, team=None)
    try:
        db_session.add(user)
        db_session.commit()
        return True, "Successfully added User {}".format(data["username"])
    except Exception as e:
        db_session.rollback()
        return False, "Could not add User {}; already exists".format(data["username"])


def modify_user(db_session, data):
    user = app_users(db_session, {"username": data["username"]})[0]
    changes = {}
    changes["username"] = data["changes"].get("username", user.username)
    changes["name"] = data["changes"].get("name", user.name)
    changes["password"] = data["changes"].get("password", user.password)

    try:
        user.username = changes["username"]
        user.name = changes["name"]
        user.password = changes["password"]
        db_session.commit()
        return True, "Successfully modified user {}".format(data["username"])
    except Exception as e:
        db_session.rollback()
        return False, e


def add_team(db_session, data):
    team = Team(name=data["name"])
    user = app_users(db_session, {"username": data["username"]})[0]
    team.members.append(user)

    try:
        db_session.add(team)
        db_session.commit()
        return True, "Successfully added Team {}".format(data["name"])
    except Exception as e:
        db_session.rollback()
        return False, "Could not add Team Exception: {}".format(e)


def join_team(db_session, data):
    team = teams(db_session, {"name": data["name"]})[0]
    user = app_users(db_session, {"username": data["username"]})[0]

    try:
        user.team = team
        db_session.commit()
        return True, "Successfully added User {} to Team {}".format(data["username"], data["name"])
    except Exception as e:
        db_session.rollback()
        return False, e
