from model.base import ModelBase
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
import datetime

class UserMessageMapping(ModelBase):
    __tablename__='users_messages_mapping'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    message_id = Column(Integer, ForeignKey('messages.id'))
    placeholder_id = Column(Integer, ForeignKey('placeholders.id'))
    is_read = Column(Integer, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now())

    def to_dict(self):
        obj_dict = super(self.__class__,self).to_dict()

        if self.user_id:
            obj_dict["user_id"] = self.user_id
        if self.message_id:
            obj_dict["message_id"] = self.message_id
        if self.placeholder_id:
            obj_dict["placeholder_id"] = self.placeholder_id
        if self.is_read:
            obj_dict["is_read"] = self.is_read
        if self.id:
            obj_dict["id"] = self.id
        if self.created_at:
            obj_dict["created_at"] = self.created_at
        if self.updated_at:
            obj_dict["updated_at"] = self.updated_at
        return obj_dict

    def to_json_dict(self, include=None):
        obj_dict = self.to_dict()
        return obj_dict

    def from_dict(self, obj_dict):
        if "user_id" in obj_dict:
            self.user_id = obj_dict["user_id"]
        if "message_id" in obj_dict:
            self.message_id = obj_dict["message_id"]
        if "placeholder_id" in obj_dict:
            self.placeholder_id = obj_dict["placeholder_id"]
        if "id" in obj_dict:
            self.id = obj_dict["id"]
        if "created_at" in obj_dict:
            self.created_at = obj_dict["created_at"]
        if "updated_at" in obj_dict:
            self.updated_at = obj_dict["updated_at"]
        return self

    def from_json_dict(self, obj_dict):
        self.from_dict(obj_dict)
        return self

    @classmethod
    def add_mapping(cls, db, dict):
        mapping_dict = UserMessageMapping().from_json_dict(dict)
        mapping_dict.created_at = datetime.datetime.now()
        mapping_dict.updated_at = datetime.datetime.now()
        db.add(mapping_dict)
        return mapping_dict

    @classmethod
    def update(cls, db, mapping_id, dict):
        query = db.query(cls)
        return query.filter(cls.id == mapping_id).update(dict)
