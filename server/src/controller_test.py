import controller
import json
import pytest
import requests
import mocks
from rest_service import slack_users
from sanic.response import HTTPResponse

######### GET TESTS ###########

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

def test_get_app_users():
    mockUser = mocks.MockUser("testuser", "testpassword", "tester", 0, "sudoers")
    mockRequest = {"username": "testuser", "team": "sudoers"}

    result = controller.get_app_users(mockRequest, mocks.MockFilterProvider(mockUser))
    data = json.loads(result.body)
    assert data['ok'] == True
    assert data['data'][0]['username'] == mockRequest["username"]

def test_get_teams():
    mockTeam = mocks.MockTeam("team1", [mocks.MockUser("testuser")])
    mockRequest = {"name": "team1"}

    result = controller.get_teams(mockRequest, mocks.MockFilterProvider(mockTeam))
    data = json.loads(result.body)
    assert data['ok'] == True
    assert data['data'][0] != None

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

######## AUTH TESTS ###########

def test_authenticate_user():
    mockUser = mocks.MockUser("testuser", "testpassword")
    mockRequest = {"username": "testuser", "password": "testpassword"}
    mockWrongRequest = {"username": "testuser"}
    correct = controller.authenticate_user(mockRequest, mocks.MockFilterProvider(mockUser))
    incorrect = controller.authenticate_user(mockWrongRequest, mocks.MockFilterProvider(mockUser))
    data = json.loads(correct.body)
    assert data['ok'] == True
    data = json.loads(incorrect.body)
    assert data['ok'] == False


######## ADD TESTS #############

def test_add_user(monkeypatch):
    class SlackUsersMock:
        def __init__(*args, **kwargs):
            return
        def json(self):
            return {
                'ok': True,
                'members': [
                    {
                        'deleted': False,
                        'name': 'snax',
                        'profile': {
                            'real_name_normalized': 'Hot Dog',
                            'image_192': 'https://fakeurl.coolbeans'
                        }
                    },
                    {
                        'deleted': False,
                        'name': 'fail',
                        'profile': {
                            'real_name_normalized': 'I should throw',
                            'image_192': 'https://fakeurl.coolbeans'
                        }
                    }
                ]
            }
    monkeypatch.setattr(requests, 'get', SlackUsersMock)
    response = controller.get_slack_users()
    assert type(response) is HTTPResponse
    assert response.status == 200

    mockRequest = {"username": "four-o-four", "password": "no"}
    noSlackResult = json.loads(controller.add_user(mockRequest, None).body)
    assert noSlackResult["ok"] == False
    assert noSlackResult["message"] == "No Slack user four-o-four"

    mockRequest = {"username": "snax", "password": "no"}
    someSlackResult = json.loads(controller.add_user(mockRequest, mocks.MockAdderDatabase()).body)
    assert someSlackResult["ok"] == True
    assert someSlackResult["data"] == "Successfully added User snax"

    mockRequest = {"username": "fail", "password": "no"}
    failSlackResult = json.loads(controller.add_user(mockRequest, mocks.MockAdderDatabase()).body)
    assert failSlackResult["ok"] == False


###### MODIFY TESTS ########


def test_add_challenge():
    controller.add_challenge(None, None)

def test_ok():
    data = {
        'hello': 'world'
    }
    assert type(controller.ok(data)) is dict
    assert controller.ok(data) == {'ok': True, 'data': {'hello': 'world'}}

def test_error():
    assert type(controller.error('oops')) is dict
    assert controller.error('oops') == {'ok': False, 'message': 'oops'}

