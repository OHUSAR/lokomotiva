from django.contrib import admin
from user_profiles.models import *

admin.site.register(UserType)
admin.site.register(ChildProfile)
admin.site.register(ParentChildren)
