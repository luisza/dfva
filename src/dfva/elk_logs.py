import os

ELK_INSTALLED_APPS = [
    'django_elasticsearch_dsl',
]


ELASTICSEARCH_DSL={
    'default': {
        'hosts':  os.getenv('ELASTICSEARCH_HOST', 'localhost:9200')
    },
}

LOGSTASH_HOST = os.getenv('LOGSTASH_HOST', 'localhost')

LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
      'simple': {
            'format': 'velname)s %(message)s'
        },
  },
  'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'logstash': {
            'level': 'WARNING',
            'class': 'logstash.TCPLogstashHandler',
            'host': LOGSTASH_HOST,
            'port': 5000, # Default value: 5959
            'version': 1, # Version of logstash event schema. Default value: 0 (for backward compatibility of the library)
            'message_type': 'django',  # 'type' field in logstash message. Default value: 'logstash'.
            'fqdn': False, # Fully qualified domain name. Default value: false.
            'tags': ['django.request'], # list of tags. Default: None.
        },
        'dfvalogstash': {
            'level': 'INFO',
            'class': 'logstash.TCPLogstashHandler',
            'host': LOGSTASH_HOST,
            'port': 5000, # Default value: 5959
            'version': 1, # Version of logstash event schema. Default value: 0 (for backward compatibility of the library)
            'message_type': 'dfva',  # 'type' field in logstash message. Default value: 'logstash'.
            'fqdn': False, # Fully qualified domain name. Default value: false.
            'tags': ['dfva.info'], # list of tags. Default: None.
        },
        'dfva_sign_auth': {
            'level': 'INFO',
            'class': 'logstash.TCPLogstashHandler',
            'host': LOGSTASH_HOST,
            'port': 5000, # Default value: 5959
            'version': 1, # Version of logstash event schema. Default value: 0 (for backward compatibility of the library)
            'message_type': 'dfvasign',  # 'type' field in logstash message. Default value: 'logstash'.
            'fqdn': False, # Fully qualified domain name. Default value: false.
            'tags': ['dfva.sign'], # list of tags. Default: None.
        },
  },
  'loggers': {
        'django.request': {
            'handlers': ['logstash'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'dfva': {
            'handlers': ['dfvalogstash'],
            'level': 'INFO',
            'propagate': True,
        },
        'soapfish':  {
            'handlers': ['dfvalogstash'],
            'level': 'INFO',
            'propagate': True,
        },
        'pyfva':  {
            'handlers': ['dfvalogstash'],
            'level': 'INFO',
            'propagate': True,
        },
        'dfva_authentication': {
            'handlers': ['dfva_sign_auth'],  # 'log/authentication',
            'level': 'INFO',
            'propagate': False,

        },
        'dfva_sign': {
            'handlers': ['dfva_sign_auth'],  # 'log/sign',
            'level': 'INFO',
            'propagate': False,

        }
    }
}
