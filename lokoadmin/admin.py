from django.contrib import admin
from user_profiles.models import *
from events.models import *

admin.site.register(UserType)
admin.site.register(ChildProfile)
admin.site.register(ParentChildren)
admin.site.register(EventType)
admin.site.register(Event)
admin.site.register(Accomodation)
admin.site.register(AttendingEvent)
