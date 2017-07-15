from sanic import Sanic
from sanic_cors import CORS, cross_origin
from config import config
import controller

app = Sanic(__name__)
CORS(app, origins=config['allowed_host_list'])

@app.route('/', methods=['GET'])
async def heartbeat(request):
    return controller.get_heartbeat(request)

@app.route('/slack-users', methods=['GET'])
async def slack_users(request):
    return controller.get_slack_users(request)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
