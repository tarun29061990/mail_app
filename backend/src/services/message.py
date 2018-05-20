from datetime import datetime
from model.message import Message
from model.user_message_mapping import UserMessageMapping
from model.placeholder import Placeholder
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

    def convert_to_message_dict(self, dict):
         return {
             "body": dict["body"] if "body" in dict else '',
             "subject": dict["subject"] if "subject" in dict else ''
         }

    def add_user_message_mapping(self, dict, placeholder_name):
        with Db.get() as self._db:
            placeholder = Placeholder.get_by_name(self._db, placeholder_name)
            mapping_dict = {
                "user_id": dict["user_id"],
                "placeholder_id": placeholder.id,
                "message_id": dict["message_id"]
            }
            user_message_mapping = UserMessageMapping.add_mapping(self._db, mapping_dict)
            self._db.commit()
            self._db.refresh(user_message_mapping)
            return user_message_mapping

    def update_user_message_mapping(self, mapping_id, dict):
        with Db.get() as self._db:
            UserMessageMapping.update(self._db, mapping_id, dict)
            self._db.commit()
            return dict