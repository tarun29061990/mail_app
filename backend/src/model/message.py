import datetime
from sqlalchemy import Column, DateTime, Integer, String, text
from sqlalchemy.orm import relationship, joinedload_all,joinedload
from model.base import ModelBase

class Message(ModelBase):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    subject = Column(String(255))
    body = Column(String(255))
    date = Column(DateTime, nullable=False, default=datetime.datetime.now())
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now())

    user = relationship("User", lazy="subquery", secondary="users_messages_mapping")

    def to_dict(self, include):
        obj_dict = super(self.__class__,self).to_dict()

        if self.subject:
            obj_dict["subject"] = self.subject
        if self.body:
            obj_dict["body"] = self.body
        if self.id:
            obj_dict["id"] = self.id
        if self.date:
            obj_dict["date"] = self.date
        if self.created_at:
            obj_dict["created_at"] = self.created_at
        if self.updated_at:
            obj_dict["updated_at"] = self.updated_at

        if include is not None and "user" in include:
            obj_dict['user'] = self.user
        return obj_dict

    def to_json_dict(self, include=None):
        obj_dict = self.to_dict(include)
        return obj_dict

    def from_dict(self, obj_dict):
        if "subject" in obj_dict:
            self.subject = obj_dict["subject"]
        if "body" in obj_dict:
            self.body = obj_dict["body"]
        if "date" in obj_dict:
            self.date = obj_dict["date"]
        if "created_at" in obj_dict:
            self.created_at = obj_dict["created_at"]
        if "updated_at" in obj_dict:
            self.updated_at = obj_dict["updated_at"]
        return self

    def from_json_dict(self, obj_dict):
        self.from_dict(obj_dict)
        return self

    @classmethod
    def add(cls, db, dict):
        message_dict = Message().from_json_dict(dict)
        message_dict.created_at = datetime.datetime.now()
        message_dict.updated_at = datetime.datetime.now()
        db.add(message_dict)
        return message_dict

    @classmethod
    def join_tables(cls, query, include):
        if not include: return query
        if "user" in include:
            query = query.options(joinedload(cls.user))
        return query

    @classmethod
    def get(cls, db, id):
        query = db.query(cls)
        return query.filter(cls.id == id).first()