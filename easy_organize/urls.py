"""easy_organize URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout


urlpatterns = [
    url(r'^login/$', login, {'template_name': 'lokoadmin/login/login.html'}, name='login'),
    url(r'^logout/$', logout, kwargs={'next_page': 'login'}, name='logout'),
    url(r'^events/', include('frontend.urls', namespace='frontend')),
    url(r'^lokoadmin/', include('lokoadmin.urls', namespace='lokoadmin')),
    url(r'^admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^', include('landing_page.urls', namespace='landing_page')),
]
