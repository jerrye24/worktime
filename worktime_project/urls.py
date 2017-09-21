#coding=utf-8
"""project0 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from worktime.views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', custom_login, name='login'),
    url(r'^logout_then_login/$', logout_then_login, name='logout_then_login'),
    url(r'^tabel/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', TabelView.as_view(), name='tabel'),
    url(r'^tabel_period_form/$', tabel_period_form, name='tabel_period_form'),
    url(r'tabel_json/$', tabel_json, name='tabel_json'),
    url(r'^tabel_period/(?P<start>\d+)/(?P<end>\d+)/(?P<id>\d+)/$', tabel_period, name='tabel_period'),
    url(r'^employee/$', employee_view, name='employee'),
    url(r'^employee_create/$', employee_create_view, name='employee_create'),
    url(r'^employee_update/(?P<pk>\d+)/$', employee_update_view, name='employee_update'),
    url(r'^employee_delete/(?P<pk>\d+)/$', EmployeeDeleteView.as_view(success_url='/employee/'), name='employee_delete'),
    url(r'^export_xlsx/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', export_xlsx, name='export_xlsx'),
]

admin.site.site_header = 'Администрирование Worktime'
admin.site.title = 'Администрирование Worktime'
admin.site.index_title = 'Worktime'
