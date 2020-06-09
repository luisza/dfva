import os

DEFAULT_LOGGER_NAME = 'dfva'
DEFAULT_LOGGER_LEVEL = 'DEBUG'
DEFAULT_LOGGER_HANDLER = ['file']
GRAY_LOG_SERVER = 'localhost'
GRAY_LOG_PORT = 12201
APP_SERVER_NAME = os.uname().nodename


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {

        'file': {
            'class': 'pygelf.GelfUdpHandler',
            'host': GRAY_LOG_SERVER,
            'port': GRAY_LOG_PORT,
            '_app_name': 'dfva',
            '_customlevel': "debug",
            '_application': APP_SERVER_NAME

        },

        'file_info_graylog': {
            'class': 'pygelf.GelfUdpHandler',
            'host': GRAY_LOG_SERVER,
            'port': GRAY_LOG_PORT,
            '_app_name': 'ucrfva',
            '_customlevel': "info",
            '_application': APP_SERVER_NAME,

        },
        'remove_authentication': {
            'class': 'pygelf.GelfUdpHandler',
            'host': GRAY_LOG_SERVER,
            'port': GRAY_LOG_PORT,
            '_app_name': 'ucrfva',
            '_customlevel': "remove_authentication",
            '_application': APP_SERVER_NAME
        },
        'remove_sign': {
            'class': 'pygelf.GelfUdpHandler',
            'host': GRAY_LOG_SERVER,
            'port': GRAY_LOG_PORT,
            '_app_name': 'ucrfva',
            '_customlevel': "remove_authentication",
            '_application': APP_SERVER_NAME
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },

    },
    'loggers': {
        DEFAULT_LOGGER_NAME: {
            'handlers':  DEFAULT_LOGGER_HANDLER,  # ['file_info'],  # 'console',
            'level': DEFAULT_LOGGER_LEVEL,

        },
        'django': {
            'handlers': DEFAULT_LOGGER_HANDLER,
            'level': DEFAULT_LOGGER_LEVEL,
            'propagate': True
        },
        'django.request': {
            'handlers': DEFAULT_LOGGER_HANDLER,
            'level': DEFAULT_LOGGER_LEVEL,
            'propagate': False,
        },
        'celery': {
            'handlers': DEFAULT_LOGGER_HANDLER,
            'level': DEFAULT_LOGGER_LEVEL,
            'propagate': True
        },
        'soapfish':  {
            'handlers': DEFAULT_LOGGER_HANDLER,
            'level': DEFAULT_LOGGER_LEVEL,

        },
        'pyfva':  {
            'handlers': DEFAULT_LOGGER_HANDLER,
            'level': DEFAULT_LOGGER_LEVEL,
        },
        'dfva_authentication': {
            'handlers': ['remove_authentication'],  # 'log/authentication',
            'level': 'INFO',
        },
        'dfva_sign': {
            'handlers': ['remove_sign'],  # 'log/sign',
            'level': 'INFO',
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(name)s %(levelname)s %(asctime)s %(module)s %(funcName)s %(process)d %(processName)s %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(module)s %(message)s'
        },
        'quiet': {
            'format': '\n--- %(asctime)s ---\n %(message)s'
        },
    },
}
