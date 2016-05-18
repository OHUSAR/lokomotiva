from django.template.defaultfilters import stringfilter
from django import template


register = template.Library()


@register.filter(name='add_attributes')
def add_attributes(field, arg):
    if arg is None:
        return field
    try:
        pairs = [arg, ]
        if ';' in arg:
            pairs = [pair.strip() for pair in arg.split(';')]
        attributes = {}
        for pair in pairs:
            name, value = [item.strip() for item in pair.split(':')]
            attributes[name] = value
    except ValueError:
        return field
    return field.as_widget(attrs=attributes)


@register.filter(is_safe=True)
@stringfilter
def add_label_class(label, arg):
    """Add a class to a label (`add_class_and_placeholder` cannot do it)."""
    assert label.find('class=') < 0  # one day this might need to change...
    return label.replace('<label', '<label class="{}"'.format(arg))
