import datetime
from model.base import ModelBase
from sqlalchemy import Column, Integer, String, DateTime

class Placeholder(ModelBase):
    __tablename__='placeholders'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    display_name = Column(String(255))
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now())

    def to_dict(self):
        obj_dict = super(self.__class__,self).to_dict()

        if self.name:
            obj_dict["name"] = self.name
        if self.display_name:
            obj_dict["display_name"] = self.display_name
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
        if "display_name" in obj_dict:
            self.display_name = obj_dict["display_name"]
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
        placeholder_dict = Placeholder().from_json_dict(dict)
        placeholder_dict.created_at = datetime.datetime.now()
        placeholder_dict.updated_at = datetime.datetime.now()
        db.add(placeholder_dict)
        return placeholder_dict

    @classmethod
    def get_by_name(cls, db, name):
        query = db.query(cls)
        return query.filter(cls.name == name).first()

