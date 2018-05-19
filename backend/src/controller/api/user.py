from app import flask, controller
from flask import request
from services.user import UserService
from util.json import json_response

@flask.route('/users', methods=['POST'])
@controller.api_controller()
def add_user():
    dict = request.get_json(force=True)
    return json_response(UserService().add(dict))