from django import template
import datetime

register = template.Library()


@register.filter()
def seconds_to_time(seconds):
    if seconds == 0:
        return '0'
    return str(datetime.timedelta(seconds=seconds))