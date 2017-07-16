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
            if not slack_user['deleted'] and \
                    slack_user['name'] not in config['blacklisted_slack_users']:
                formatted_slack_user = {
                    'username': slack_user['name'],
                    'realname': slack_user['profile']['real_name_normalized'],
                    'avatar': slack_user['profile']['image_192']
                }
                formatted_slack_users.append(formatted_slack_user)
        return json(ok(formatted_slack_users))

def ok(data):
    return {'ok': True, 'data': data}

def error(message):
    return {'ok': False, 'message': message}

