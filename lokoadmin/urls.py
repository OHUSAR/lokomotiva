from django.conf.urls import url
from lokoadmin.views.dashboard import *
from user_profiles.views import *
from events.views import *

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

attendance_urls = [
    url(r'^events/child_attendance/$', child_attendance, name='child_attendance'),
]

event_urls = [
    url(r'^events/$', events, name='events'),
    url(r'^events/older/(.+)/(.*)/$', events, name='events'),
    url(r'events/(?P<pk>[0-9]+)/$', EventDetail.as_view(), name='event_detail'),
    url(r'events/(?P<pk>[0-9]+)/users/$', event_users, name='event_users'),
    url(r'events/(?P<pk>[0-9]+)/clone/$', event_clone, name='event_clone'),
    url(
        r'events/(?P<pk>[0-9]+)/accomodation/$',
        event_accomodation, name='event_accomodation'
    ),
    url(
        r'events/(?P<pk>[0-9]+)/payments/$',
        event_payment, name='event_payment'
    ),
    url(
        r'events/(?P<pk>[0-9]+)/payments/(?P<payment_pk>[0-9]+)/delete/$',
        delete_payment, name='delete_payment'
    ),
    url(
        r'events/(?P<pk>[0-9]+)/payments/(?P<payment_pk>[0-9]+)$',
        event_payment, name='event_payment'
    ),
    url(
        r'events/(?P<pk>[0-9]+)/payments/(?P<payment_pk>[0-9]+)/edit$',
        edit_payment, name='edit_payment'
    ),
    url(
        r'events/(?P<pk>[0-9]+)/payments/add/$',
        add_payment, name='add_payment'
    ),
    url(
        r'events/(?P<pk>[0-9]+)/accomodation/(?P<accomodation_pk>[0-9]+)/delete/$',
        delete_accomodation, name='delete_accomodation'
    ),
    url(
        r'events/(?P<pk>[0-9]+)/accomodation/(?P<accomodation_pk>[0-9]+)$',
        event_accomodation, name='event_accomodation'
    ),
    url(
        r'events/(?P<pk>[0-9]+)/accomodation/(?P<accomodation_pk>[0-9]+)/edit$',
        edit_accomodation, name='edit_accomodation'
    ),
    url(
        r'events/(?P<pk>[0-9]+)/accomodation/add/$',
        add_accomodation, name='add_accomodation'
    ),
    url(r'events/add/$', EventAdd.as_view(), name='event_add'),
    url(r'events/(?P<pk>[0-9]+)/edit/$', EventEdit.as_view(), name='event_edit'),
    url(r'events/(?P<pk>[0-9]+)/delete/$', EventDelete.as_view(), name='event_delete'),
]

event_type_urls = [
    url(r'^events/types/$', EventTypeList.as_view(), name='event_types'),
    url(r'events/types/add/$', EventTypeAdd.as_view(), name='event_type_add'),
    url(r'events/types/(?P<pk>[0-9]+)/$', EventTypeEdit.as_view(), name='event_type_edit'),
    url(r'events/types/(?P<pk>[0-9]+)/delete/$', EventTypeDelete.as_view(), name='event_type_delete'),
]

urlpatterns = dashboard_urls + user_profile_urls + event_urls + event_type_urls + attendance_urls
