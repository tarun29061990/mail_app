from app import flask, controller
from flask import request
from util.json import json_response
from services.mail import MailService

@flask.route('/mail', methods=['POST'])
@controller.api_controller()
def compose_mail():
    dict = request.get_json(force=True)
    return json_response(MailService().compose(dict))

@flask.route('/mail/<mapping_id>', methods=['DELETE'])
@controller.api_controller()
def delete_mail(mapping_id):
    return json_response(MailService().delete(mapping_id))

@flask.route('/mail/<mapping_id>', methods=['PUT'])
@controller.api_controller()
def save_to_drafts(mapping_id):
    return json_response(MailService().save_to_drafts(mapping_id))