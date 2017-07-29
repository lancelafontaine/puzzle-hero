from config import config
from sanic.response import json
import rest_service


def get_heartbeat(request=None):
    return json(ok('hello world'))


def get_slack_users(request=None):
    slack_users_response = rest_service.slack_users().json()
    if not slack_users_response['ok']:
        return json(error('Slack API error'), status=504)
    else:
        formatted_slack_users = []
        for slack_user in slack_users_response['members']:
            if not slack_user['deleted'] and slack_user['name'] not in config['blacklisted_slack_users']:
                formatted_slack_user = {
                    'username': slack_user['name'],
                    'realname': slack_user['profile']['real_name_normalized'],
                    'avatar': slack_user['profile']['image_192']
                }
                formatted_slack_users.append(formatted_slack_user)
        return json(ok(formatted_slack_users))


def get_app_users(request, session):
    users_response = rest_service.app_users(session)

    users = [{
             'username': user.username,
             'name': user.name,
             'score': user.score,
             'team': user.team
             } for user in users_response]

    return json(ok(users))


def add_user(request, session):
    # super preliminary
    request = request.json
    data = {
        "username": request["username"],
        "name": request["name"],  # this should actually be retrieved from slack
        "password": request["password"]
    }
    result = rest_service.add_user(session, data)
    return json(ok(result)) if result else json(error(result))


def add_challenge(request, session):
    pass


def ok(data):
    return {'ok': True, 'data': data}


def error(message):
    return {'ok': False, 'message': message}
