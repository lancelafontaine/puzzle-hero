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

def post_validate_slack_email(request):
    slack_users_response = rest_service.slack_users().json()
    if not slack_users_response['ok']:
        return json(error('Slack API error'), status=504)
    slack_user_to_email = None
    user_data = request.json
    print(user_data)
    print(type(user_data))
    for slack_user in slack_users_response['members']:
        if not slack_user['deleted'] and \
                slack_user['name'] not in config['blacklisted_slack_users']:
                # user_data.get('username') == slack_user['name']:
            slack_user_to_email = slack_user
            break

    # TODO: Should write a user to db here as an attempted registration
    # - username: VARCHAR
    # - SALTED ENCRYPTED PASSWORD: VARCHAR?
    # - registered: FALSE
    # - last_attempted_registration: CURRENT DATE
    # - confirmation_code: VARCHAR (random string)

    # TODO: Make sure that user is not already registered!
    # If so, return here, front-end should show prompt to reset password

    # TODO: Make sure that the password is long enough
    # If so, return here, front-end should refuse registration

    return json(ok(request.json))

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
