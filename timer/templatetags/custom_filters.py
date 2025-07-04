# optional enhancement for better styling
from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def add_class(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter
def format_duration(duration):
    """Formats a timedelta object into HH:MM:SS."""
    if not isinstance(duration, timedelta):
        return ""  # Return empty string if not a timedelta object

    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"