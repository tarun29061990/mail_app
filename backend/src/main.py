import logging
import os

import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../vendor"))

from app import flask as application
# noinspection PyUnresolvedReferences
import controller

logging.info("Python version: " + sys.version)
logging.info("Current directory: " + os.getcwd())


if __name__ == '__main__':
    application.run(host="0.0.0.0", port=4000, debug=True)
