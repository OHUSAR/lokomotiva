from django.conf.urls import url
from frontend.views import *


dashboard_urls = [
    url(r'^$', dashboard, name='dashboard'),
    url(r'^date/(.+)/$', dashboard, name='dashboard'),
    url(r'^event/(.+)/$', event_detail, name='event')
]

urlpatterns = dashboard_urls
