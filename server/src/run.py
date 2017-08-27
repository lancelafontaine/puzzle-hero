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
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


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

@app.route('/authenticate-user', methods=['GET'])
async def authenticate_user(request):
    return controller.authenticate_user(request.json, db_session)


@app.route("/users", methods=["GET"])
async def users(request):
    return controller.get_app_users(request.json, db_session)


@app.route("/teams", methods=["GET"])
async def teams(request):
    return controller.get_teams(request.json, db_session)


@app.route("/modify-user", methods=["POST"])
async def modify_user(request):
    return controller.modify_user(request.json, db_session)


@app.route("/add-user", methods=["POST"])
async def add_user(request):
    return controller.add_user(request.json, db_session)


@app.route("/add-team", methods=["POST"])
async def add_team(request):
    return controller.add_team(request.json, db_session)


@app.route("/join-team", methods=["POST"])
async def join_team(request):
    return controller.join_team(request.json, db_session)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
