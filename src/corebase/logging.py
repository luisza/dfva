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
@date: 25/8/2017
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''


def get_ip(request):
    #  try:
    #             real_ip = request.META['HTTP_X_FORWARDED_FOR']
    #         except KeyError:
    #             pass
    #         else:
    #             # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs.
    #             # Take just the first one.
    #             real_ip = real_ip.split(",")[0]
    #             #request.META['REMOTE_ADDR'] = real_ip
    return request.META.get('REMOTE_ADDR')


def get_log_institution_information(request):
    data = request.data
    ip = get_ip(request)
    institution = data.get('institution', 'N/D')
    data_hash = data.get('data_hash', 'hash not found')
    algorithm = data.get('algorithm',  'Algorithm not found')
    return ip, institution, data_hash, algorithm


def get_log_person_information(request):
    data = request.data
    ip = get_ip(request)
    person = data.get('person', 'N/D')
    data_hash = data.get('data_hash', 'hash not found')
    algorithm = data.get('algorithm',  'Algorithm not found')
    return ip, person, data_hash, algorithm
