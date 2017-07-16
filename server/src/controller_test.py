import json
import controller
from sanic.response import HTTPResponse

def test_get_heartbeat():
    assert type(controller.get_heartbeat(None)) is HTTPResponse
    assert controller.get_heartbeat(None).status == 200
    data = json.loads(controller.get_heartbeat(None).body)
    assert data == {'data': 'hello world', 'ok': True}

