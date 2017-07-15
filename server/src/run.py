from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS, cross_origin

allowed_host_list = [
    'http://localhost:8080'
]

app = Sanic(__name__)
CORS(app, origins=allowed_host_list)

@app.route("/")
async def test(request):
    return json({"hello": "world"})

@app.route("/slack-users")
async def test(request):
    return json({"hello": "world"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
