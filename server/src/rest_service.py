from config import config
import requests

def slack_users():
    token_data = {'token': config['slackToken']}
    return requests.get(config['slackApiUrl'] + '/users.list', params=token_data)

