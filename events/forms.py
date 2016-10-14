from django.forms import Form
from django.utils.translation import ugettext_lazy as _
from events.models import *
from django.forms.models import *
from django import forms
import datetime

REQUIRED = _("Toto je povinná položka.")
UNIQUE = _("Takýto záznam už existuje.")
MAX_LENGTH = _("Prekročili ste maximálnu dĺžku reťazca.")
DATE = _("Zadajte správny formát dátumu.")


class EventTypeForm(ModelForm):
    class Meta:
        model = EventType
        fields = ('name', )
        labels = {
            'name': _('Názov')
        }
        error_messages = {
            'name': {
                'required': REQUIRED,
                'unique': UNIQUE,
                'max_length': MAX_LENGTH
            }
        }


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = (
            'type',
            'name',
            'location',
            'max_capacity',
            'start_date',
            'start_time',
            'end_date',
            'end_time',
            'signup_end_date',
            'signup_end_time',
            'description',
        )
        labels = {
            'type': _('Typ'),
            'name': _('Názov'),
            'location': _('Miesto konania'),
            'max_capacity': _("Kapacita"),
            'start_date': _('Dátum začiatku'),
            'start_time': _('Čas začiatku'),
            'end_date': _('Dátum konca'),
            'end_time': _('Čas konca'),
            'signup_end_date': _('Dátum konca prihlasovania'),
            'signup_end_time': _('Čas konca prihlasovania'),
            'description': _('Popis'),
        }
        error_messages = {
            'type': {
                'required': REQUIRED,
            },
            'name': {
                'required': REQUIRED,
                'max_length': MAX_LENGTH
            },
            'location': {
                'required': REQUIRED,
                'max_length': MAX_LENGTH
            },
            'max_capacity': {
                'required': REQUIRED,
            },
            'start_date': {
                'required': REQUIRED,
            },
            'start_time': {
                'required': REQUIRED,
            },
            'end_date': {
                'required': REQUIRED,
            },
            'end_time': {
                'required': REQUIRED,
            },
            'signup_end_date': {
                'required': REQUIRED,
            },
            'signup_end_time': {
                'required': REQUIRED,
            },
            'description': {
                'required': REQUIRED,
            },
        }


class AccomodationForm(ModelForm):
    class Meta:
        model = Accomodation
        fields = (
            'location',
            'start_date',
            'end_date',
            'price_per_night',
            'description',
        )
        labels = {
            'location': _('Miesto / názov'),
            'start_date': _('Dátum začiatku'),
            'end_date': _('Dátum konca'),
            'price_per_night': _("Cena za noc"),
            'description': _('Popis'),
        }
        error_messages = {
            'location': {
                'required': REQUIRED,
                'max_length': MAX_LENGTH
            },
            'price_per_night': {
                'required': REQUIRED,
            },
            'start_date': {
                'required': REQUIRED,
            },
            'end_date': {
                'required': REQUIRED,
            },
            'description': {
                'required': REQUIRED,
            },
        }


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = (
            'name',
            'price',
            'due_date',
        )
        labels = {
            'name': _('Popis'),
            'due_date': _('Dátum začiatku'),
            'price': _("Cena"),
        }
        error_messages = {
            'name': {
                'required': REQUIRED,
                'max_length': MAX_LENGTH
            },
            'due_date': {
                'required': REQUIRED,
            },
            'price': {
                'required': REQUIRED,
            },
        }


"""
-----------------
DOCHADZKA
-----------------
"""


class ChildAttendanceForm(Form):
    start_date = forms.DateField(initial=datetime.date.today)
    end_date = forms.DateField(initial=datetime.date.today)
    type = ModelChoiceField(queryset=EventType.objects.all())
