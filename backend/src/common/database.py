import logging
from contextlib import contextmanager

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from common.conf import Conf
from util.common import DatetimeUtil


class Db(object):
    __Session = None
    __instance = None

    @staticmethod
    def get_instance():
        if Db.__instance is None:
            Db.__instance = Db()
        return Db.__instance

    def init(self, conf_key="database"):
        if not conf_key: conf_key = "database"
        Db.__Session = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=self.get_engine(conf_key=conf_key))
        logging.debug("DbConfig initialized")

    def get_engine(self, conf_key="database"):
        db_conf = Conf.get(conf_key)
        db_baseurl = "mysql://%s/%s?charset=%s&user=%s&passwd=%s" % (
            db_conf["host"], db_conf["name"], db_conf["charset"], db_conf["user"], db_conf["password"])
        logging.info("DB Baseurl: %s, Init pool size: %s, Max pool size: %s, Pool recycle delay: %s" % (
            db_baseurl, db_conf["init_pool_size"], db_conf["max_pool_size"], db_conf["pool_recycle_delay"]))
        return create_engine(db_baseurl, echo=db_conf["sql_logging"], poolclass=QueuePool,
                             pool_size=db_conf["init_pool_size"],
                             max_overflow=int(db_conf["max_pool_size"]) - int(db_conf["init_pool_size"]),
                             pool_recycle=db_conf["pool_recycle_delay"])

    def __get_session(self):
        return Db.__Session()

    @staticmethod
    def get_db():
        return Db.get_instance().__get_session()

    @staticmethod
    @contextmanager
    def get():
        start_time = datetime.datetime.now()
        db = Db.get_db()
        logging.debug("Connection time: %s milliseconds" % DatetimeUtil.diff(start_time, datetime.datetime.now()))

        try:
            yield db
        except:
            db.rollback()
            raise
        finally:
            db.close()


class EventDb(object):
    __Session = None
    __instance = None

    @staticmethod
    def get_instance():
        if EventDb.__instance is None:
            EventDb.__instance = EventDb()
        return EventDb.__instance

    def init(self):
        EventDb.__Session = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=self.get_engine())
        logging.debug("DbConfig initialized")

    def get_engine(self):
        db_conf = Conf.get("event_database")
        db_baseurl = "mysql://%s/%s?charset=%s&user=%s&passwd=%s" % (
            db_conf["host"], db_conf["name"], db_conf["charset"], db_conf["user"], db_conf["password"])
        logging.info("DB Baseurl: %s, Init pool size: %s, Max pool size: %s, Pool recycle delay: %s" % (
            db_baseurl, db_conf["init_pool_size"], db_conf["max_pool_size"], db_conf["pool_recycle_delay"]))
        return create_engine(db_baseurl, echo=db_conf["sql_logging"], poolclass=QueuePool,
                             pool_size=db_conf["init_pool_size"],
                             max_overflow=int(db_conf["max_pool_size"]) - int(db_conf["init_pool_size"]),
                             pool_recycle=db_conf["pool_recycle_delay"])

    def __get_session(self):
        return EventDb.__Session()

    @staticmethod
    def get_db():
        return EventDb.get_instance().__get_session()

    @staticmethod
    @contextmanager
    def get():
        start_time = datetime.datetime.now()
        db = EventDb.get_db()
        logging.debug("Connection time: %s milliseconds" % DatetimeUtil.diff(start_time, datetime.datetime.now()))

        try:
            yield db
        except:
            db.rollback()
            raise
        finally:
            db.close()


class DBQueryHandler(object):
    @staticmethod
    def get(db, query, one=False):
        cur = db.execute(query)
        rv = cur.fetchall()
        cur.close()
        rows = []
        for row in rv:
            rows.append(dict(zip(row.keys(), row)))

        return (rows[0] if rows else None) if one else rows

    @staticmethod
    def get_all(db, query, one=False):
        cur = db.execute(query)
        rv = cur.fetchall()
        cur.close()
        rows = []
        for row in rv:
            rows.append(row[0])
        return (rows[0] if rows else None) if one else rows

    @staticmethod
    def update(db, query):
        cur = db.execute(query)
        cur.close()
