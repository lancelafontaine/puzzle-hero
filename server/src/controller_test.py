import controller
import json
import pytest
import requests
from rest_service import slack_users
from sanic.response import HTTPResponse

class OneResult:
    def __init__(self, result = None):
        self.result = result
    def one(self):
        return self.result

class ShallowFilter:
    def __init__(self, anything = None):
        self.dataToReturn = anything
    def filter(self, any):
        return OneResult(self.dataToReturn)
    def filter_by(self, **any):
        return [self.dataToReturn]

class UserMockProvider:
    def __init__(self, user = None):
        self.user = user
    def query(self, any):
        return ShallowFilter(self.user)

class MockUser:
    def __init__(self, username = None, password = None, name = None, score = None, team = None):
        self.username = username
        self.password = password
        self.team_name = team
        self.score = score
        self.name = name

def test_get_heartbeat():
    assert type(controller.get_heartbeat()) is HTTPResponse
    assert controller.get_heartbeat().status == 200
    data = json.loads(controller.get_heartbeat(None).body)
    assert data == {'data': 'hello world', 'ok': True}

def test_get_slack_users_slack_api_error(monkeypatch):
    class SlackUsersMock:
        def __init__(*args, **kwargs):
            return
        def json(self):
            return {
                'ok': False,
                'members': []
            }
    monkeypatch.setattr(requests, 'get', SlackUsersMock)
    assert type(controller.get_slack_users()) is HTTPResponse
    assert controller.get_slack_users().status == 504
    data = json.loads(controller.get_slack_users().body)
    assert data == {'message': 'Slack API error', 'ok': False}

def test_authenticate_user():
    mockUser = MockUser("testuser", "testpassword")
    mockRequest = {"username": "testuser", "password": "testpassword"}
    mockWrongRequest = {"username": "testuser"}
    correct = controller.authenticate_user(mockRequest, UserMockProvider(mockUser))
    incorrect = controller.authenticate_user(mockWrongRequest, UserMockProvider(mockUser))
    data = json.loads(correct.body)
    assert data['ok'] == True
    data = json.loads(incorrect.body)
    assert data['ok'] == False

def test_get_app_users():
    mockUser = MockUser("testuser", "testpassword", "tester", 0, "sudoers")
    mockRequest = {"username": "testuser", "team": "sudoers"}

    result = controller.get_app_users(mockRequest, UserMockProvider(mockUser))
    data = json.loads(result.body)
    assert data['ok'] == True
    assert data['data'][0]['username'] == mockRequest["username"]

def test_get_slack_users_no_users(monkeypatch):
    class SlackUsersMock:
        def __init__(*args, **kwargs):
            return
        def json(self):
            return {
                'ok': True,
                'members': []
            }
    monkeypatch.setattr(requests, 'get', SlackUsersMock)
    assert type(controller.get_slack_users()) is HTTPResponse
    assert controller.get_slack_users().status == 200
    data = json.loads(controller.get_slack_users().body)
    assert data == {'data': [], 'ok': True}

def test_get_slack_users_filters_deleted_and_blacklisted(monkeypatch):
    class SlackUsersMock:
        def __init__(*args, **kwargs):
            return
        def json(self):
            return {
                'ok': True,
                'members': [
                    {
                        'deleted': True,
                        'name': 'snax',
                        'profile': {
                            'real_name_normalized': 'Hot Dog',
                            'image_192': 'https://fakeurl.coolbeans'
                        }
                    },
                    {
                        'deleted': False,
                        'name': 'testuser',
                        'profile': {
                            'real_name_normalized': 'Will BeFiltered',
                            'image_192': 'https://fakeurl.coolbeans'
                        }
                    },
                    {
                        'deleted': False,
                        'name': 'real_user',
                        'profile': {
                            'real_name_normalized': 'Bloop Bloop',
                            'image_192': 'https://fakeurl.coolbeans'
                        }
                    }
                ]
            }
    monkeypatch.setattr(requests, 'get', SlackUsersMock)
    assert type(controller.get_slack_users()) is HTTPResponse
    assert controller.get_slack_users().status == 200
    data = json.loads(controller.get_slack_users().body)
    assert data == {
        'data': [{
            'username': 'real_user',
            'realname': 'Bloop Bloop',
            'avatar': 'https://fakeurl.coolbeans',

        }],
        'ok': True
    }

def test_ok():
    data = {
        'hello': 'world'
    }
    assert type(controller.ok(data)) is dict
    assert controller.ok(data) == {'ok': True, 'data': {'hello': 'world'}}

def test_error():
    assert type(controller.error('oops')) is dict
    assert controller.error('oops') == {'ok': False, 'message': 'oops'}

