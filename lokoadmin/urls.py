from django.conf.urls import url
from lokoadmin.views.dashboard import *
from user_profiles.views import *
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
    url(r'^users/add$', add_user, name='add_user'),
]

urlpatterns = auth_urls + dashboard_urls + user_profile_urls
