from functools import wraps
from sanic.response import json
from helpers import ok

def responds_to_options():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if request.method == 'OPTIONS':
                return json(ok({}))
            response = await f(request, *args, **kwargs)
            return response
        return decorated_function
    return decorator
