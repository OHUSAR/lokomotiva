from django.conf.urls import url
from landing_page.views import *


dashboard_urls = [
    url(r'^$', landing_view, name='landing_page'),
]

urlpatterns = dashboard_urls
