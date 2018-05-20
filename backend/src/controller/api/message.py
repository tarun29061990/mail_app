from app import flask, controller
from services.message import MessageService
from flask import request
from util.json import json_response

@flask.route('/messages', methods=['POST'])
@controller.api_controller()
def add_message():
    dict = request.get_json(force=True)
    return json_response(MessageService().add(dict))

@flask.route('/messages/<int:id>', methods=['GET'])
@controller.api_controller()
def get_message(id):
    include = ['user','parent','children']
    return json_response(MessageService().get(id, include),include)

@flask.route('/messages/<int:id>', methods=['PUT'])
@controller.api_controller()
def update_message(id):
    dict = request.get_json(force=True)
    return json_response(MessageService().update_user_message_mapping(id, dict))