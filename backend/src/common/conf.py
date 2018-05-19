import logging
import os
from logging import config

import yaml

MIME_TYPE_JSON = "application/json"


class Conf(object):
    __instance = None

    ROOT_FOLDER = None

    def __init__(self):
        self.app_conf = None

    @staticmethod
    def get_instance():
        if Conf.__instance is None:
            Conf.__instance = Conf()
        return Conf.__instance

    def init(self, curr_dir):
        Conf.ROOT_FOLDER = os.path.abspath(curr_dir + "/..")

        stream = open(Conf.ROOT_FOLDER + "/conf/logging.yaml", "r")
        config.dictConfig(yaml.load(stream))
        stream.close()
        logging.debug("Logging initialized")

        stream = open(Conf.ROOT_FOLDER + "/conf/app.yaml", "r")
        self.app_conf = yaml.load(stream)
        stream.close()
        logging.debug("Config initialized")

        logging.info("ROOT_FOLDER: %s" % Conf.ROOT_FOLDER)

    def get_value(self, key):
        return self.app_conf[key]

    def set_value(self, key, value):
        self.app_conf[key] = value

    @staticmethod
    def get(key):
        return Conf.get_instance().get_value(key)

    @staticmethod
    def set(key, value):
        Conf.get_instance().set_value(key, value)


class URLConf(object):
    @staticmethod
    def get_studio_ui_baseurl(secure=False):
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        return scheme + Conf.get("studio_ui")["base_url"]

    @staticmethod
    def get_launchpad_api_baseurl(secure=False):
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        return scheme + Conf.get("launchpad_api_host")

    @staticmethod
    def get_bouncer_api_baseurl(secure=False):
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        return scheme + Conf.get("bouncer")["host"]

    @staticmethod
    def get_oms_api_baseurl(secure=False):
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        oms = Conf.get("oms")
        return scheme + oms["host"]

    @staticmethod
    def get_cms_api_baseurl(secure=False):
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        cms = Conf.get("cms")
        return scheme + cms["host"]

    @staticmethod
    def get_pms_api_baseurl(secure=False):
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        oms = Conf.get("pms")
        return scheme + oms["host"]

    @staticmethod
    def get_website_api_baseurl(secure=False):
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        return scheme + Conf.get("website")["host"]

    @staticmethod
    def get_livspace_boqapi_baseurl(secure=False):
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        return scheme + Conf.get("boq")["host"]

    @staticmethod
    def get_livspace_catalog_baseurl(secure=False):
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        return scheme + Conf.get("catalog")["host"]

    @staticmethod
    def get_launchpad_admin_baseurl(secure=False):
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        return scheme + Conf.get("launchpad_admin_app_host")

    @staticmethod
    def get_designer_ui_baseurl(secure=False):
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        return scheme + Conf.get("designer_ui_app_host")

    @staticmethod
    def get_livspace_oms_baseurl(secure=False):
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        return scheme + Conf.get("livspace_oms_api_host")

    @staticmethod
    def get_livspace_cms_baseurl(secure=False):
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        return scheme + Conf.get("livspace_cms_api_host")

    @staticmethod
    def get_livspace_pms_baseurl(secure=False):
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        return scheme + Conf.get("livspace_pms_api_host")

    @staticmethod
    def get_mom_baseurl(secure=False):
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        return scheme + Conf.get("mom_base_url")

    @staticmethod
    def get_cdn_baseurl(secure=False):
        cdn = Conf.get("cdn")
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        if cdn["enabled"]:
            return scheme + Conf.get("cdn")["base_url"]
        else:
            return scheme + Conf.get("cdn")["s3_base_url"] + "/" + Conf.get("amazon_aws")["s3_bucket_images"]

    @staticmethod
    def get_lego_api_baseurl(secure=False):
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        lego = Conf.get("lego")
        return scheme + lego["host"]

    @staticmethod
    def get_calendar_service_baseurl(secure=False):
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        calendar = Conf.get("livspace_calendar")["host"]
        return scheme + calendar

    @staticmethod
    def get_tasker_service_baseurl(secure=False):
        if secure:
            scheme = "https://"
        else:
            scheme = "http://"
        tasker = Conf.get("tasker_web")["host"]
        return scheme + tasker
