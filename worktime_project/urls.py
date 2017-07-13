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
from worktime import views
from worktime.views import *

urlpatterns = [
	url(r'^$', views.index, name='index'),
        url(r'^admin/', admin.site.urls),
        url(r'^login/$', views.custom_login, name='login'),
        url(r'^logout_then_login/$', logout_then_login, name='logout_then_login'),
        url(r'^tabel/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', TabelView.as_view(), name='tabel'),
        url(r'^tabel_period_form/$', views.tabel_period_form, name='tabel_period_form'),
        url(r'^tabel_period/(?P<start>\d+)/(?P<end>\d+)/(?P<id>\d+)/$', views.tabel_period, name='tabel_period'),
        url(r'^employee/$', EmployeeView.as_view(), name='employee'),
        url(r'^employee/(\w)/', EmployeeSearchView.as_view(), name='search'),
        url(r'^employee_create/$', employee_create_view, name='employee_create'),
        url(r'^employee_update/(?P<pk>\d+)/$', employee_update_view, name='employee_update'),
        url(r'^employee_delete/(?P<pk>\d+)/$', EmployeeDeleteView.as_view(success_url='/employee/'), name='employee_delete'),
        url(r'^export_xlsx/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.export_xlsx, name='export_xlsx'),
]
