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
