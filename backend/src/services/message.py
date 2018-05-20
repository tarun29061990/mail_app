from datetime import datetime
from model.message import Message
from model.user import User
from model.user_message_mapping import UserMessageMapping
from model.placeholder import Placeholder
from common.database import Db
from services.common import DatabaseService

class MessageService(DatabaseService):
    def get(self, message_id, include):
        with Db.get() as self._db:
            return Message.get(self._db, message_id, include)


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
             "subject": dict["subject"] if "subject" in dict else '',
             "creator_id":dict["creator_id"] if "creator_id" in dict else ''
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

    def get_user_message_mapping(self, user_id, placeholder_name=None):
        with Db.get() as self._db:
            placeholder = Placeholder.get_by_name(self._db, placeholder_name)
            user = User.get(self._db, user_id)

            if len(user):
                user_dict = user[0].to_json_dict()
                user_message_mappings = UserMessageMapping.get_mapping(self._db, user_id)

                mapping_arr = []
                for umm in user_message_mappings:
                    if umm.placeholder_id == placeholder.id:
                        message = Message.get(self._db, umm.message_id)
                        umm_dict = umm.to_json_dict()
                        umm_dict["message"] = message.to_json_dict()
                        mapping_arr.append(umm_dict)

                user_dict['mp'] = mapping_arr

                return user_dict

    def update_message(self, id, dict):
        with Db.get() as self._db:
            Message.update(self._db, id, dict)
            self._db.commit()
            return dict