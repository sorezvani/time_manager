
# In your template filters (optional enhancement for better styling)
from django import template
register = template.Library()

@register.filter
def add_class(field, css):
    return field.as_widget(attrs={"class": css})
