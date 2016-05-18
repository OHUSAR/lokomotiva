from django.contrib.auth.models import User
from django.db.models import *
from django.utils.translation import ugettext_lazy as _


USER_TYPES = ((0, _("parent")),
              (1, _("child")),
              (2, _("trainer")))


class UserType(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    user_type = IntegerField(choices=USER_TYPES, verbose_name="typ užívateľa")


class ChildProfile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    first_name = CharField(max_length=50, verbose_name="meno")
    last_name = CharField(max_length=50, verbose_name="priezvisko")
    birthday = DateField(verbose_name="dátum narodenia")
    member_since = DateField(verbose_name="vstup do klubu", auto_now=True)


class ParentProfile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    first_name = CharField(max_length=50, verbose_name="meno")
    last_name = CharField(max_length=50, verbose_name="priezvisko")
    children = ManyToManyField(ChildProfile, related_name="parents", verbose_name="deti")


class TrainerProfile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    first_name = CharField(max_length=50, verbose_name="meno")
    last_name = CharField(max_length=50, verbose_name="priezvisko")
