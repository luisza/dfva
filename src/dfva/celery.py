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
@date: 11/9/2017
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from __future__ import absolute_import

import os
from urllib.parse import quote
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      os.getenv('DJANGO_SETTINGS_MODULE', 'dfva.settings'))

from django.conf import settings  # noqa

if settings.DOCKER:
    RABBIT_USER = os.getenv('RABBIT_USER', 'guest')
    RABBIT_PASS = quote(os.getenv('RABBIT_PASS', 'password'), safe='')
    RABBIT_HOST = os.getenv('RABBIT_HOST', 'rabbitmq')
    RABBIT_PORT = os.getenv('RABBIT_PORT', '5672')
    RABBIT_VHOST = os.getenv('RABBIT_VHOST', 'myhost')
    app = Celery('dfva', broker='amqp://%s:%s@%s:%s/%s'%(RABBIT_USER, RABBIT_PASS, RABBIT_HOST, RABBIT_PORT, RABBIT_VHOST), backend='rpc://' )
else:
    app = Celery('dfva')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
