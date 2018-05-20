from services.common import DatabaseService
from services.message import MessageService
from common.database import Db
from model.user import User
from bcrypt import hashpw, gensalt
from flask_login import login_user, LoginManager
from app import flask, controller
flask.config['SECRET_KEY'] = 'thisissecret'

login_manager = LoginManager()
login_manager.init_app(flask)

class UserService(DatabaseService):
    def add(self, dict):
        with Db.get() as self._db:
            if "password" in dict:
                dict["password"] = hashpw(dict["password"].encode('utf8'), gensalt())
            user = User.add(self._db,dict)
            self._db.commit()
            self._db.refresh(user)
            return user

    def get_by_email(self, email):
        with Db.get() as self._db:
            user = User.get_by_email(self._db, email)
            return user[0].to_json_dict()

    def login(self, dict):
        with Db.get() as self._db:
            user = User.get_by_email(self._db, dict["email"])
            user_dict = user[0].to_json_dict(include=['password'])

            if hashpw(dict['password'].encode('utf-8'), user_dict['password'].encode('utf-8')).decode('utf-8') == user_dict['password']:
                login_user(user[0])
                return user
            else:
                return {'message':'Incorrect Password'}

    def get_placeholder_mails(self, user_id, placeholder_name):
        with Db.get() as self._db:
            return MessageService().get_user_message_mapping(user_id, placeholder_name)