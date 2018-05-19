import logging
import datetime

from common.conf import Conf, URLConf
from util.common import HttpUtil
# from cachetools import TTLCache, cached
#
# cache = TTLCache(maxsize=512, ttl=300)

class Service(object):
    pass


class DatabaseService(Service):
    def __init__(self, db=None):
        self._db = db

    def _bulk_save_objects(self, model_list):
        self._db.bulk_save_objects(model_list)

    def _add(self, model):
        model.id = None
        model.created_at = datetime.datetime.now()
        model.updated_at = datetime.datetime.now()
        self._db.add(model)
        return model

    def _update(self, model):
        model.updated_at = datetime.datetime.now()
        model = self._db.merge(model)
        return model
