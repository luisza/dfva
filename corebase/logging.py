'''
Created on 25 ago. 2017

@author: luis
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
