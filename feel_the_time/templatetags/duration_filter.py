from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def format_timedelta(value):
    if isinstance(value, timedelta):
        total_sec = value.total_seconds()
        hours, reminder = divmod(total_sec, 3600)
        minutes, seconds = divmod(reminder, 60)
        result = ''
        if hours:
            result += f"{int(hours)} часов "
        if minutes:
            result += f"{int(minutes)} минут "
        return result + f"{int(seconds)} секунд"
    return value