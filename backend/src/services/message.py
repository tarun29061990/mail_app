from datetime import datetime
from model.message import Message
from common.database import Db
from services.common import DatabaseService

class MessageService(DatabaseService):
    def add(self, dict):
        with Db.get() as self._db:
            dict["date"] = datetime.now()
            message = Message.add(self._db, dict)
            self._db.commit()
            self._db.refresh(message)
            return message