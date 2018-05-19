from app import flask, controller
from services.message import MessageService
from flask import request
from util.json import json_response

@flask.route('/messages', methods=['POST'])
@controller.api_controller()
def add_message():
    dict = request.get_json(force=True)
    return json_response(MessageService().add(dict))