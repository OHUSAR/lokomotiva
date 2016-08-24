from django import template
from events.api import is_accomodated

register = template.Library()


@register.filter
def check(accomodation, user):
    return "selected" if is_accomodated(user, accomodation) else ""
