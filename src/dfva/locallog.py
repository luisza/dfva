import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(BASE_DIR)

LOG_BASE_DIR = os.environ.get('LOG_BASE_DIR', BASE_DIR+'/logs/')
os.makedirs(LOG_BASE_DIR, exist_ok=True)

DEFAULT_LOGGER_NAME = 'dfva'
DEFAULT_LOGGER_LEVEL = 'DEBUG'
DEFAULT_LOGGER_HANDLER = ['file']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_BASE_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_BASE_DIR, 'info.log'),
            'formatter': 'simple',
        },
        'remove_authentication': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_BASE_DIR, 'authentication.log'),
            'formatter': 'quiet',
        },
        'remove_sign': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_BASE_DIR, 'sign.log'),
            'formatter': 'quiet',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },

    },
    'loggers': {
        DEFAULT_LOGGER_NAME: {
            'handlers': ['file_info'],  # 'console',
            'level': 'INFO',
            'propagate': True,
        },
        'soapfish':  {
            'handlers': ['file_info'],
            'level': 'INFO',
            'propagate': True,
        },
        'pyfva':  {
            'handlers': ['file_info'],
            'level': 'INFO',
            'propagate': True,
        },
        'dfva_authentication': {
            'handlers': ['remove_authentication'],  # 'log/authentication',
            'level': 'INFO',
            'propagate': False,

        },
        'dfva_sign': {
            'handlers': ['remove_sign'],  # 'log/sign',
            'level': 'INFO',
            'propagate': False,

        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(module)s %(message)s'
        },
        'quiet': {
            'format': '\n--- %(asctime)s ---\n %(message)s'
        },
    },
}