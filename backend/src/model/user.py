import datetime
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship, lazyload, joinedload_all, joinedload
from model.base import ModelBase
from flask_login import LoginManager, UserMixin

class User(ModelBase):
    __tablename__='users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(255))
    password = Column(String(255))
    is_authenticated = UserMixin.is_authenticated
    is_active = UserMixin.is_active
    is_anonymous = UserMixin.is_anonymous
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now())

    def to_dict(self):
        obj_dict = super(self.__class__,self).to_dict()

        if self.name:
            obj_dict["name"] = self.name
        if self.email:
            obj_dict["email"] = self.email
        if self.password:
            obj_dict["password"] = self.password
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
        if "name" in obj_dict:
            self.name = obj_dict["name"]
        if "email" in obj_dict:
            self.email = obj_dict["email"]
        if "password" in obj_dict:
            self.password = obj_dict["password"]
        if "created_at" in obj_dict:
            self.created_at = obj_dict["created_at"]
        if "updated_at" in obj_dict:
            self.updated_at = obj_dict["updated_at"]
        return self

    def from_json_dict(self, obj_dict):
        self.from_dict(obj_dict)
        return self

    @classmethod
    def add(cls,db,dict):
        user_dict = User().from_json_dict(dict)
        user_dict.created_at = datetime.datetime.now()
        user_dict.updated_at = datetime.datetime.now()
        db.add(user_dict)
        return user_dict

    @classmethod
    def get(cls,db,id):
        query = db.query(cls)
        return query.filter(cls.id == id).all()

    @classmethod
    def get_by_email(cls,db,email):
        query = db.query(cls)
        return query.filter(cls.email == email).all()

    @classmethod
    def delete(cls,db,id):
        query = db.query(cls)
        return query.filter(cls.id == id).delete()