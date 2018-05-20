from app import flask, controller
from flask import request
from services.user import UserService
from util.json import json_response

@flask.route('/users', methods=['POST'])
@controller.api_controller()
def add_user():
    dict = request.get_json(force=True)
    return json_response(UserService().add(dict))

@flask.route('/login', methods=['POST'])
@controller.api_controller()
def login():
    dict = request.get_json(force=True)
    return json_response(UserService().login(dict))

@flask.route('/users/<int:id>/<string:placeholder_name>', methods=['GET'])
@controller.api_controller()
def get_placeholder_mails(id, placeholder_name):
    return json_response(UserService().get_placeholder_mails(id, placeholder_name))