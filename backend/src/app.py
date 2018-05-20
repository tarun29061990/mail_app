import os

from flask import Flask

from common.conf import Conf

from common.database import Db, EventDb
from common.decorator import Controller, Permissions, Security

from flask_cors import CORS

flask = Flask(__name__, template_folder="templates", static_folder="../static")
CORS(flask)

Conf.get_instance().init(os.path.dirname(os.path.realpath(__file__)))
Db.get_instance().init()

controller = Controller.get_instance()
# permissions = Permissions.get_instance()
security = Security.get_instance()


