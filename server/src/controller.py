from config import config
from sanic import response
import rest_service


def get_heartbeat(request=None):
    return ok('hello world')


def get_slack_users(request=None):
    slack_users_response = rest_service.slack_users().json()
    if not slack_users_response['ok']:
        return error('Slack API error')

    formatted_slack_users = []
    for slack_user in slack_users_response['members']:
        if not slack_user['deleted'] and slack_user['name'] not in config['blacklisted_slack_users']:
            formatted_slack_user = {
                'username': slack_user['name'],
                'realname': slack_user['profile']['real_name_normalized'],
                'avatar': slack_user['profile']['image_192']
            }
            formatted_slack_users.append(formatted_slack_user)
    return ok(formatted_slack_users)


def authenticate_user(request, db_session):
    if "username" not in request or "password" not in request:
        return error("Malformed authenticate_user request")

    succeeded, message = rest_service.authenticate_user(db_session, request)
    result = ok if succeeded else error
    return result(message)


def get_app_users(request, db_session):
    query_filter = {}
    if "username" in request:
        query_filter["username"] = request["username"]
    if "team" in request:
        query_filter["team_name"] = request["team"]

    users_response = rest_service.app_users(db_session, query_filter)
    users = [{
             'username': user.username,
             'name': user.name,
             'score': user.score,
             'team': user.team_name
             } for user in users_response]

    return ok(users)


def get_teams(request, db_session):
    query_filter = {}
    if "name" in request:
        query_filter["name"] = request["name"]

    teams_response = rest_service.teams(db_session, query_filter)
    teams = [{
             'name': team.name,
             'members': [user.username for user in team.members]
             } for team in teams_response]

    return ok(teams)


def add_user(request, db_session):
    data = {
        "username": request["username"],
        "password": request["password"]
    }
    slack_users = rest_service.slack_users().json()
    slack_users = [user for user in slack_users['members'] if user["name"] == request["username"]]

    if not slack_users or slack_users[0]['deleted'] or slack_users[0]['name'] in config['blacklisted_slack_users']:
        return error("No Slack user {}".format(request["username"]))

    data["name"] = slack_users[0]['profile']['real_name_normalized']

    succeeded, message = rest_service.add_user(db_session, data)
    result = ok if succeeded else error
    return result(message)


def modify_user(request, db_session):
    succeeded, message = rest_service.modify_user(db_session, request)
    result = ok if succeeded else error
    return result(message)


def add_team(request, db_session):
    if "name" not in request or "username" not in request:
        return error("Malformed request: {}".format(request))

    succeeded, message = rest_service.add_team(db_session, request)
    result = ok if succeeded else error
    return result(message)


def join_team(request, db_session):
    if "name" not in request or "username" not in request:
        return error("Malformed request: {}".format(request))

    succeeded, message = rest_service.join_team(db_session, request)
    result = ok if succeeded else error
    return result(message)


def add_challenge(request, db_session):
    pass


def ok(data, code=200):
    return response.json({'ok': True, 'data': data}, status=code)

def error(message, code=504):
    return response.json({'ok': False, 'message': message}, status=code)
