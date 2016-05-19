from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db.models import *
from tinymce.models import HTMLField


class EventType(Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('lokoadmin:event_types')


class Event(Model):
    type = ForeignKey(EventType, on_delete=CASCADE)
    name = CharField(max_length=100)
    location = CharField(max_length=100)
    start_date = DateField()
    start_time = TimeField()
    end_date = DateField()
    end_time = TimeField()
    description = HTMLField()

    max_capacity = PositiveIntegerField()
    signup_end_date = DateField()
    signup_end_time = TimeField()

    def get_absolute_url(self):
        return reverse('lokoadmin:event_detail', args=[self.pk, ])

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError("Udalosť nemôže skončiť skôr, ako začne.")


class Accomodation(Model):
    event = OneToOneField(Event, on_delete=CASCADE)
    start_date = DateField()
    end_date = DateField()
    location = CharField(max_length=100)
    price_per_night = DecimalField(max_digits=10, decimal_places=2)
    description = HTMLField()


class AttendingEvent(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name='events')
    event = ForeignKey(Event, on_delete=CASCADE, related_name='attending')

    class Meta:
        unique_together = ('user', 'event')
