from pyboot.db import DatabaseModel
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query
from sqlalchemy.orm import Session

from util.common import Parser, DatetimeUtil, Validator, DateUtil

TYPE_INT = "int"
TYPE_FLOAT = "float"
TYPE_BOOL = "bool"
TYPE_STR = "str"
TYPE_DATETIME = "datetime"
TYPE_DATE = "date"
TYPE_OBJ = "obj"
TYPE_RELATION = "relation"
TYPE_ENUM = "enum"
TYPE_UNKNOWN = "unknown"


class JSONSerializable(object):
    def to_json_dict(self, include: list = None) -> dict:
        return {}

    def from_json_dict(self, json_dict: dict):
        return self


class HttpResponse(JSONSerializable):
    def __init__(self, code: int = 0, message: str = "Success"):
        self.code = code
        self.message = message

    def to_json_dict(self, include: list = None):
        json_dict = super().to_json_dict(include)
        json_dict["code"] = self.code
        json_dict["message"] = self.message
        return json_dict


class Page(JSONSerializable):
    def __init__(self):
        self.items = []
        self.count = 0
        self.total_count = 0

        self.is_prev_page = False
        self.prev_page_start = None
        self.prev_page_count = None
        self.prev_page_url = None

        self.is_next_page = False
        self.next_page_start = None
        self.next_page_count = None
        self.next_page_url = None

    def gen_page_data(self, start: int, count: int):
        if start > 0:
            self.is_prev_page = True
            if start >= count:
                self.prev_page_start = start - count
                self.prev_page_count = count
            else:
                self.prev_page_start = 0
                self.prev_page_count = start
        else:
            self.is_prev_page = False

        if len(self.items) > count:
            self.is_next_page = True
            if start + count <= self.total_count - count:
                self.next_page_start = start + count
                self.next_page_count = count
            else:
                self.next_page_start = start + count
                self.next_page_count = self.total_count - self.next_page_start
            self.items = self.items[:-1]
        else:
            self.is_next_page = False
        self.count = len(self.items)

    # def gen_page_urls(self, baseurl: str, params: dict):
    #     clean_params = DictUtil.delete_null_values(params)
    #     params_str = ""
    #     for key in clean_params:
    #         params_str += "&" + key + "=" + clean_params[key]
    #
    #     if self.is_prev_page:
    #         self.prev_page_url = "%s?start=%s&count=%s%s" % (
    #             baseurl, self.prev_page_start, self.prev_page_count, params_str)
    #
    #     if self.is_next_page:
    #         self.next_page_url = "%s?start=%s&count=%s%s" % (
    #             baseurl, self.next_page_start, self.next_page_count, params_str)

    def to_json_dict(self, include: list = None):
        json_dict = super().to_json_dict(include)
        json_dict["count"] = self.count
        if isinstance(self.items, list):
            json_dict["items"] = []
            for item in self.items:
                if isinstance(item, JSONSerializable):
                    json_dict["items"].append(item.to_json_dict(include))
                else:
                    json_dict["items"].append(item)
        else:
            json_dict["items"] = self.items
        json_dict["total_count"] = self.total_count
        json_dict["is_prev"] = self.is_prev_page
        json_dict["is_next"] = self.is_next_page
        return json_dict


class Model(JSONSerializable):
    _fields = None

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)  # type: int

    @classmethod
    def _query(cls, query: Query, start: int = None, count: int = None, order_by=None) -> Query:
        if start: query = query.offset(start)
        if count: query = query.limit(count)
        if order_by is not None: query = query.order_by(order_by)
        return query

    @classmethod
    def get_all(cls, db: Session, start: int = None, count: int = None, order_by=None, include: list = None) -> list:
        query = cls._query(db.query(cls), start=start, count=count, order_by=order_by)
        cls.join_tables(query, include)
        return query.all()

    @classmethod
    def get(cls, db: Session, id: int, include: list = None):
        query = db.query(cls)  # type: Query
        query = cls.join_tables(query, include)
        return query.get(id)

    @classmethod
    def delete(cls, db: Session, id: int):
        db.query(cls).filter(cls.id == id).delete()

    @classmethod
    def join_tables(cls, query: Query, include: list = None) -> Query:
        return query

    def _to_dict_field(self, obj_dict, name: str, type: str = None):
        if type == TYPE_RELATION or not name or not hasattr(self, name): return
        value = getattr(self, name, None)
        if type == TYPE_STR:
            obj_dict[name] = Parser.str(value)
        elif type == TYPE_INT:
            obj_dict[name] = Parser.int(value)
        elif type == TYPE_FLOAT:
            obj_dict[name] = Parser.float(value)
        elif type == TYPE_BOOL:
            obj_dict[name] = Parser.bool(value)
        elif type == TYPE_DATETIME:
            if isinstance(value, str):
                obj_dict[name] = DatetimeUtil.iso_to_dt_local(value)
            else:
                obj_dict[name] = Validator.datetime(value)
        elif type == TYPE_DATE:
            if isinstance(value, str):
                obj_dict[name] = DateUtil.iso_to_date(value)
            else:
                obj_dict[name] = Validator.date(value)
        else:
            obj_dict[name] = value

    def _from_dict_field(self, obj_dict, name: str, type: str = None):
        if type == TYPE_RELATION or not name or name not in obj_dict or not hasattr(self, name): return
        value = obj_dict.get(name)
        if type == TYPE_STR:
            setattr(self, name, Parser.str(value))
        elif type == TYPE_INT:
            setattr(self, name, Parser.int(value))
        elif type == TYPE_FLOAT:
            setattr(self, name, Parser.float(value))
        elif type == TYPE_BOOL:
            setattr(self, name, Parser.bool(value))
        elif type == TYPE_DATETIME:
            if isinstance(value, str):
                setattr(self, name, DatetimeUtil.iso_to_dt_local(value))
            else:
                setattr(self, name, Validator.datetime(value))
        elif type == TYPE_DATE:
            if isinstance(value, str):
                setattr(self, name, DateUtil.iso_to_date(value))
            else:
                setattr(self, name, Validator.date(value))
        else:
            setattr(self, name, value)

        return None

    def to_dict(self):
        obj_dict = {}
        if self.id: obj_dict["id"] = self.id
        if self.__class__._fields:
            for field_name in self.__class__._fields.keys():
                self._to_dict_field(obj_dict, field_name, self.__class__._fields[field_name])
        return obj_dict

    def from_dict(self, obj_dict: dict):
        if not obj_dict: return
        if "id" in obj_dict: self.id = obj_dict["id"]
        if self.__class__._fields:
            for field_name in self.__class__._fields.keys():
                self._from_dict_field(obj_dict, field_name, self.__class__._fields[field_name])
        return self

    def to_json_dict(self, include: list = None) -> dict:
        json_dict = self.to_dict()
        if self.__class__._fields:
            for field_name in self.__class__._fields.keys():
                if self.__class__._fields[field_name] != TYPE_RELATION: continue
                self._include_obj(json_dict, include, field_name)
        return json_dict

    def from_json_dict(self, json_dict: dict):
        self.from_dict(json_dict)
        if self.__class__._fields:
            for field_name in self.__class__._fields:
                if self.__class__._fields[field_name] != TYPE_RELATION: continue
                self._exclude_obj(json_dict, field_name)
        return self

    def _include_obj(self, json_dict: dict, include: list, name: str):
        if not include: include = []
        field_name = name + "_id"

        sub_obj = getattr(self, name, None) if name in include else None
        value = getattr(self, field_name, None)
        if sub_obj:
            if isinstance(sub_obj, Model): json_dict[name] = sub_obj.to_dict()
            elif isinstance(sub_obj, DatabaseModel): json_dict[name] = sub_obj.to_dict()
        elif value:
            json_dict[name] = {"id": value}
        elif name in include:
            json_dict[name] = None

        if field_name in json_dict: del json_dict[field_name]

    def _exclude_obj(self, json_dict: dict, name: str):
        if not json_dict: return
        if name in json_dict and "id" in json_dict[name]:
            setattr(self, name + "_id", json_dict[name]["id"])


ModelBase = declarative_base(cls=Model)
