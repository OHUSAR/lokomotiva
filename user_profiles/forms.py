from user_profiles.models import *
from django.forms import ModelForm, PasswordInput, DateInput, CheckboxSelectMultiple
from django.utils.translation import ugettext_lazy as _


REQUIRED = _("Toto je povinná položka.")
UNIQUE = _("Takýto záznam už existuje.")
MAX_LENGTH = _("Prekročili ste maximálnu dĺžku reťazca.")
DATE = _("Zadajte správny formát dátumu.")


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        widgets = {
            'password': PasswordInput,
        }
        labels = {
            'username': _('Prihlasovacie meno'),
            'email': _('Email'),
            'password': _('Heslo'),
            'first_name': _('Krstné meno'),
            'last_name': _('Priezvisko')
        }
        error_messages = {
            'username': {
                'unique': UNIQUE,
                'required': REQUIRED,
                'max_length': MAX_LENGTH
            },
            'password': {
                'required': REQUIRED
            },
            'first_name': {
                'max_length': MAX_LENGTH
            },
            'lastname': {
                'max_length': MAX_LENGTH
            },
        }


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = {
            'username': _('Prihlasovacie meno'),
            'email': _('Email'),
            'first_name': _('Krstné meno'),
            'last_name': _('Priezvisko')
        }
        error_messages = {
            'username': {
                'unique': UNIQUE,
                'required': REQUIRED,
                'max_length': MAX_LENGTH
            },
            'first_name': {
                'max_length': MAX_LENGTH
            },
            'lastname': {
                'max_length': MAX_LENGTH
            },
        }


class ChildProfileForm(ModelForm):
    class Meta:
        model = ChildProfile
        exclude = ('user', )
        labels = {
            'birthday': _('Dátum narodenia'),
            'member_since': _('V klube od')
        }
        error_messages = {
            'birthday': {
                'required': REQUIRED,
                'invalid_type': DATE
            },
            'member_since': {
                'required': REQUIRED,
                'invalid_type': DATE
            }
        }
        widgets = {
            'date': DateInput(format='%m. %d. %Y'),
            'memeber_since': DateInput(format='%m. %d. %Y'),
        }


class ParentChildrenForm(ModelForm):
    class Meta:
        model = ParentChildren
        exclude = ('user', )

        widgets = {
            'children': CheckboxSelectMultiple,
        }
