from services.common import DatabaseService
from common.database import Db
from model.user import User
from bcrypt import hashpw, gensalt

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
            return user.to_json_dict()