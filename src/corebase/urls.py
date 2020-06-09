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
@date: 18/7/2017
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from django.conf.urls import url

from corebase.reports.serialtime import show_timeperminute
from corebase.views import check_ok
from pyfva.receptor.ws_service import ResultadoDeSolicitudSoap_SERVICE
from corebase.bccr_checks import soap_dispatcher
from django.conf import settings
from corebase.reports import views as stats

dispatcher = soap_dispatcher(ResultadoDeSolicitudSoap_SERVICE)

developurl = r'^wcfv2\/Bccr\.Sinpe\.Fva\.EntidadDePruebas\.Notificador\/ResultadoDeSolicitud\.asmx$'
if settings.ONLY_BCCR:
    developurl = r'^$'

urlpatterns = [
    url('^check$', check_ok, name="check_ok"),
    url(settings.DEFAULT_NOTIFICATION_URL, dispatcher, name='ws_receptor'),
    url("corebase_stats", stats.render_stats, name="index_stats"),
    url("durations_stats", stats.get_durations_stats, name="durations_stats"),
    url("get_total_stats", stats.get_total_stats, name="total_stats"),
    url("get_error_stats", stats.get_error_stats, name="error_stats"),
    url("get_size_stats", stats.get_size_stats, name="size_stats"),
    url("total_per_minute", show_timeperminute, name="total_per_minute"),

    url(developurl, dispatcher, name='ws_receptor'),
]
