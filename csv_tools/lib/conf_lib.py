
try:
    from configparser import RawConfigParser
except ImportError:
    from ConfigParser import RawConfigParser

import openerplib
import logging
import sys


def get_server_connection(config_file):
    config = RawConfigParser({'protocol': 'jsonrpc', 'port': 8069, 'uid': 1})
    config.read(config_file)

    hostname = config.get('Connection', 'hostname')
    database = config.get('Connection', 'database')
    protocol = config.get('Connection', 'protocol')
    port = int(config.get('Connection', 'port'))
    uid = int(config.get('Connection', 'uid'))
    login = config.get('Connection', 'login')
    password = config.get('Connection', 'password')

    return openerplib.get_connection(hostname=hostname, database=database, login=login, password=password, protocol=protocol, port=port, user_id=uid)


def init_logger():
    logger_err = logging.getLogger('Error')
    logger_err.setLevel(logging.INFO)
    err = logging.StreamHandler(sys.stderr)
    logger_err.addHandler(err)
    logger = logging.getLogger('Info')
    logger.setLevel(logging.INFO)
    out = logging.StreamHandler(sys.stdout)
    logger.addHandler(out)


def log_info(msg):
    logging.getLogger('Info').info(msg)


def log_error(msg):
    logging.getLogger('Error').info(msg)


def log(msg):
    log_info(msg)
    log_error(msg)


init_logger()
