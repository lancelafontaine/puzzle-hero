from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS, cross_origin
from config import config
import controller
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from decorators import responds_to_options

app = Sanic(__name__)
CORS(app, origins=config['allowed_host_list'])

engine = create_engine('sqlite:///app.db')
Base = declarative_base()
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/', methods=['GET'])
async def heartbeat(request):
    return controller.get_heartbeat(request)


@app.route('/slack-users', methods=['GET'])
async def slack_users(request):
    return controller.get_slack_users(request)

@app.route('/validate-slack-email', methods=['POST', 'OPTIONS'])
@responds_to_options()
async def validate_slack_email(request):
    return controller.post_validate_slack_email(request)

@app.route("/users", methods=["GET"])
async def users(request):
    return controller.get_app_users(request, session)


@app.route("/add_user", methods=["POST", "OPTIONS"])
@responds_to_options()
async def users(request):
    return controller.add_user(request, session)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
