from django.conf.urls import include, url
from django.contrib import admin
from bailout.views import index, data, links, member_search

urlpatterns = [
    url(r'^$', index),
    url(r'^data$', data),
    url(r'^links$', links),
    url(r'^member_search$', member_search)
]