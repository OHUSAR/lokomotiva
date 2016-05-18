from django.core.urlresolvers import reverse
from django.db.models import *


class EventType(Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('lokoadmin:event_types')
