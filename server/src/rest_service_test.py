import pytest
import rest_service
import requests

def test_slack_users(monkeypatch):
    data = {
        'ok': True,
        'members': []
    }
    class SlackUsersMock:
        def __init__(self, *args, **kwargs):
            self.data = data
            self.status = 200
        def json(self):
            return self.data

    monkeypatch.setattr(requests, 'get', SlackUsersMock)
    assert rest_service.slack_users().json() == data
    assert rest_service.slack_users().status == 200
