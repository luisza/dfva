# encoding: utf-8

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''
@date: 1/01/2019
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''


import os

ELASTICSEARCH_DSL={
    'default': {
        'hosts':  os.getenv('ELASTICSEARCH_HOST', 'localhost:9200')
    },
}

LOGSTASH_HOST = os.getenv('LOGSTASH_HOST', 'localhost')
LOGSTASH_PORT = int(os.getenv('LOGSTASH_HOST', '5000'))
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
      'verbose': {
          'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
      },
      'simple': {
          'format': '%(levelname)s %(message)s'
      },
  },
  'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'logstash': {
            #'level': 'INFO',
            'class': 'logstash.TCPLogstashHandler',
            'host': LOGSTASH_HOST,
            'port': LOGSTASH_PORT, # Default value: 5959
            'version': 1, # Version of logstash event schema. Default value: 0 (for backward compatibility of the library)
            'message_type': 'django',  # 'type' field in logstash message. Default value: 'logstash'.
            'fqdn': False, # Fully qualified domain name. Default value: false.
            'tags': ['django.request'], # list of tags. Default: None.
        },
        'dfvalogstash': {
           # 'level': 'INFO',
            'class': 'logstash.TCPLogstashHandler',
            'host': LOGSTASH_HOST,
            'port': LOGSTASH_PORT, # Default value: 5959
            'version': 1, # Version of logstash event schema. Default value: 0 (for backward compatibility of the library)
            'message_type': 'dfva',  # 'type' field in logstash message. Default value: 'logstash'.
            'fqdn': False, # Fully qualified domain name. Default value: false.
            'tags': ['dfva.info'], # list of tags. Default: None.
        },
        'dfva_sign_auth': {
            'level': 'INFO',
            'class': 'logstash.TCPLogstashHandler',
            'host': LOGSTASH_HOST,
            'port': LOGSTASH_PORT, # Default value: 5959
            'version': 1, # Version of logstash event schema. Default value: 0 (for backward compatibility of the library)
            'message_type': 'dfvasign',  # 'type' field in logstash message. Default value: 'logstash'.
            'fqdn': False, # Fully qualified domain name. Default value: false.
            'tags': ['dfva.sign'], # list of tags. Default: None.
        },
  },
  'loggers': {
        'root': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'django.server': {
            'handlers': ['logstash', 'console'],
            'level': 'DEBUG',
            'propagate': False,
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
            'level': 'WARNING',
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
