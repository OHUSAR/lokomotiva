from django.conf.urls import url
from lokoadmin.views.dashboard import *
from django.contrib.auth.views import login, logout


auth_urls = [
    url(r'^login/$', login, {'template_name': 'lokoadmin/login/login.html'},
        name='login'),
    url(r'^logout/$', logout, kwargs={'next_page': 'lokoadmin:login'},
        name='logout')
]

dashboard_views = [
        url(r'^$', dashboard_view, name='dashboard'),
]

urlpatterns = auth_urls + dashboard_views
