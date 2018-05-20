from app import flask, controller
from flask import request
from util.json import json_response
from services.mail import MailService

@flask.route('/compose', methods=['POST'])
@controller.api_controller()
def compose_mail():
    dict = request.get_json(force=True)
    return json_response(MailService().compose(dict))

@flask.route('/mail/<mapping_id>', methods=['DELETE'])
@controller.api_controller()
def delete_mail(mapping_id):
    return json_response(MailService().delete(mapping_id))

@flask.route('/save-mail', methods=['POST'])
@controller.api_controller()
def save_to_drafts():
    dict = request.get_json(force=True)
    return json_response(MailService().save_to_drafts(dict))