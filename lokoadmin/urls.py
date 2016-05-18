from django.conf.urls import url
from lokoadmin.views.dashboard import *
from user_profiles.views import *
from events.views import *
from django.contrib.auth.views import login, logout


auth_urls = [
    url(r'^login/$', login, {'template_name': 'lokoadmin/login/login.html'},
        name='login'),
    url(r'^logout/$', logout, kwargs={'next_page': 'lokoadmin:login'},
        name='logout')
]

dashboard_urls = [
    url(r'^$', dashboard_view, name='dashboard'),
]

user_profile_urls = [
    url(r'^users/$', users, name='users'),
    url(r'^users/decide/$', user_decider, name='user_decider'),
    url(r'^users/add/(.+)/$', add_user, name='add_user'),
    url(r'^users/edit/(.+)/$', edit_user, name='edit_user'),
    url(r'^users/delete/(.+)/$', delete_user, name='delete_user'),
    url(r'^users/profile/(.+)/$', user_profile, name='user_profile'),
]

event_urls = [
    url(r'^events/$', events, name='events'),
]

event_type_urls = [
    url(r'^events/types/$', EventTypeList.as_view(), name='event_types'),
    url(r'events/types/add/$', EventTypeAdd.as_view(), name='event_type_add'),
    url(r'events/types/(?P<pk>[0-9]+)/$', EventTypeEdit.as_view(), name='event_type_edit'),
    url(r'events/types/(?P<pk>[0-9]+)/delete/$', EventTypeDelete.as_view(), name='event_type_delete'),
]

urlpatterns = auth_urls + dashboard_urls + user_profile_urls + event_urls + event_type_urls
