import logging
from enum import Enum
from urllib.parse import urlparse

from common.conf import Conf
from util.api import ApiFilters
from util.common import Parser, DatetimeUtil


def send_api_response_time(prefix, start_time, end_time, url_rule, request_method, request_url):
    try:
        statsd_conf = Conf.get("statsd")
        if not statsd_conf["enabled"]:
            logging.info("Statsd disabled, not sending stats")
            return

        if not url_rule:
            logging.info("URL rule not found for url: [%s %s]" % (request_method, request_url))
            return

        components = []
        for c in url_rule.rule.split("/"):
            if not c: continue
            if c.startswith("<int:") and c.endswith(">"):
                components.append(c[5:-1])
            elif c.startswith("<path:") and c.endswith(">"):
                components.append(c[6:-1])
            elif c.startswith("<") and c.endswith(">"):
                components.append(c[1:-1])
            else:
                components.append(c)
        if not components or len(components) <= 0: components = ["home"]

        key = prefix + "." + ".".join(components) + "." + request_method
        delta = int((end_time - start_time).total_seconds() * 1000)

        logging.debug(
                "Sending stats to %s:%s [%s: %s]" % (statsd_conf["host"], statsd_conf["port"], key, delta))

        statsd_client = StatsdClient(statsd_conf["host"], statsd_conf["port"])
        statsd_client.timing(key, delta)
    except Exception as e:
        logging.error("Error in sending stats: %s" % e)

def get_query_string(request):
    parse_object = urlparse(request.url)
    query_params = ""
    if len(parse_object.query) > 0:
        query_params = "?" + parse_object.query
    return query_params


class DBProjectFilterTypeEnum(Enum):
    INT_LIST = "INT_LIST"
    LIST = "LIST"
    DATETIME = "DATETIME"
    INT = "INT"
    STR = "STR"
    STR_UPPER = "STR_UPPER"


class DBProjectReportFilter(object):
    API_FILTER_TO_PROJECT_DB_FILTER_MAP = {
        "collaborator_id": {"db_filter_name": "collaborator_id", "type": DBProjectFilterTypeEnum.INT_LIST, "default": None},
        "city_id": {"db_filter_name": "city_id", "type": DBProjectFilterTypeEnum.INT_LIST, "default": None},
        "stage_id": {"db_filter_name": "stage_id", "type": DBProjectFilterTypeEnum.INT_LIST, "default": None},
        "stage": {"db_filter_name": "stage", "type": DBProjectFilterTypeEnum.STR, "default": None},
        "designer_type_id": {"db_filter_name": "designer_type_id", "type": DBProjectFilterTypeEnum.INT_LIST, "default": None},
        "project_type": {"db_filter_name": "project_type", "type": DBProjectFilterTypeEnum.LIST, "default": None},
        "lead_source_id": {"db_filter_name": "lead_source_id", "type": DBProjectFilterTypeEnum.INT_LIST, "default": None},
        "priority": {"db_filter_name": "priority", "type": DBProjectFilterTypeEnum.LIST, "default": None},
        "status": {"db_filter_name": "status", "type": DBProjectFilterTypeEnum.STR_UPPER, "default": None},
        "created_at_start": {"db_filter_name": "created_at_start", "type": DBProjectFilterTypeEnum.DATETIME, "default": None},
        "created_at_end": {"db_filter_name": "created_at_end", "type": DBProjectFilterTypeEnum.DATETIME, "default": None},
        "next_interaction_date_start": {"db_filter_name": "next_interaction_date_start", "type": DBProjectFilterTypeEnum.DATETIME, "default": None},
        "next_interaction_date_end": {"db_filter_name": "next_interaction_date_end", "type": DBProjectFilterTypeEnum.DATETIME, "default": None},
        "conversion_probability": {"db_filter_name": "conversion_probability", "type": DBProjectFilterTypeEnum.STR, "default": None},
        "initial_briefing_date_start": {"db_filter_name": "initial_briefing_date_start", "type": DBProjectFilterTypeEnum.DATETIME, "default": None},
        "initial_briefing_date_end": {"db_filter_name": "initial_briefing_date_end", "type": DBProjectFilterTypeEnum.DATETIME, "default": None},
        "deactivation_start_date": {"db_filter_name": "deactivation_start_date", "type": DBProjectFilterTypeEnum.DATETIME, "default": None},
        "deactivation_end_date": {"db_filter_name": "deactivation_end_date", "type": DBProjectFilterTypeEnum.DATETIME, "default": None},
    }

    @staticmethod
    def get_db_filter_from_api_filters(filters: ApiFilters):
        response_filters = {}
        for key in filters.get_all_keys():
            if key not in DBProjectReportFilter.API_FILTER_TO_PROJECT_DB_FILTER_MAP:
                continue
            type = DBProjectReportFilter.API_FILTER_TO_PROJECT_DB_FILTER_MAP[key]["type"]
            db_filter_name = DBProjectReportFilter.API_FILTER_TO_PROJECT_DB_FILTER_MAP[key]["db_filter_name"]
            default = DBProjectReportFilter.API_FILTER_TO_PROJECT_DB_FILTER_MAP[key]["default"]
            if type == DBProjectFilterTypeEnum.INT_LIST:
                response_filters[db_filter_name] = Parser.int_list(filters.get_all(key), default)
            elif type == DBProjectFilterTypeEnum.LIST:
                response_filters[db_filter_name] = Parser.list(filters.get_all(key), default)
            elif type == DBProjectFilterTypeEnum.INT:
                response_filters[db_filter_name] = Parser.int(filters.get(key), default)
            elif type == DBProjectFilterTypeEnum.STR:
                response_filters[db_filter_name] = Parser.str(filters.get(key), default)
            elif type == DBProjectFilterTypeEnum.STR_UPPER:
                response_filters[db_filter_name] = Parser.str_upper(filters.get(key), default)
            elif type == DBProjectFilterTypeEnum.DATETIME:
                response_filters[db_filter_name] = DatetimeUtil.iso_to_dt_local(filters.get(key))

        return response_filters
