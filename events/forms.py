from django.forms import Textarea
from django.utils.translation import ugettext_lazy as _
from events.models import *
from django.forms.models import *


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
