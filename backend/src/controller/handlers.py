import datetime
import json
import logging
import re

from flask import request, g, redirect

from app import flask
from controller.helpers import send_api_response_time
from model.base import HttpResponse
from util.json import json_response


@flask.errorhandler(404)
def not_found(code):
    logging.info("Page not found [%s %s]: %s" % (request.method, request.url, code.code))
    return json_response(HttpResponse(code=code.code, message="Not found")), code.code


@flask.errorhandler(Exception)
def server_error(e):
    code = 500
    logging.error("Internal error [%s %s]: %s" % (request.method, request.url, e))
    logging.exception(e)
    return json_response(HttpResponse(code=code, message="Internal error")), code


@flask.before_request
def before_request():
    g.request_start_time = datetime.datetime.now()
    g.requested_by_id = request.headers.get("X-Requested-By")
    g.request_id = request.headers.get("X-Request-Id")
    old_url = request.url
    new_url = re.sub('/api/','/',request.url)
    if old_url != new_url:
        url = request.url.replace(old_url, new_url)
        return redirect(url)
    logging.info("Before request called for [%s %s]" % (request.method, request.url))



@flask.after_request
def after_request(response):
    logging.debug("After request called for [%s %s: %s" % (request.method, request.url, request.url_rule))
    response.headers["Access-Control-Allow-Origin"]="*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "DELETE,POST,PUT,GET"
    send_api_response_time("grexter-backend", g.request_start_time, datetime.datetime.now(), request.url_rule,
                           request.method, request.url)
    return response
