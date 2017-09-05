import helpers

def test_ok():
    data = {
        'hello': 'world'
    }
    assert isinstance(helpers.ok(data), dict)
    assert helpers.ok(data) == {'ok': True, 'data': {'hello': 'world'}}

def test_error():
    assert isinstance(helpers.error('oops'), dict)
    assert helpers.error('oops') == {'ok': False, 'message': 'oops'}


