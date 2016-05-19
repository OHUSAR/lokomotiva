from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import *
from django.utils.translation import ugettext_lazy as _


USER_TYPES = ((0, _("trainer")),
              (1, _("child")),
              (2, _("parent")))


class UserType(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    user_type = IntegerField(choices=USER_TYPES, verbose_name="typ užívateľa")


class ChildProfile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    birthday = DateField(verbose_name="dátum narodenia")
    member_since = DateField(verbose_name="vstup do klubu")

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def clean(self):
        if self.birthday and self.member_since:
            if self.birthday > self.member_since:
                raise ValidationError("Dieťa nemôže byť členom skôr, ako sa narodí.")


class ParentChildren(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    children = ManyToManyField(ChildProfile, related_name="parents", verbose_name="deti",
                               blank=True)
