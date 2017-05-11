# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^api/v1/', include('mediterra.api')),
    url(r'^admin/', admin.site.urls),
]
