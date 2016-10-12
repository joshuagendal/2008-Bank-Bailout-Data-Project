from django.conf.urls import include, url
from django.contrib import admin
from bailout.views import index, data, links, member_search, financial_services_committee, switchers, no_no, yes_yes, register, user_login, user_dashboard
urlpatterns = [
    url(r'^$', index),
    url(r'^data$', data),
    url(r'^links$', links),
    url(r'^member_search$', member_search),
    url(r'^financial_services_committee$', financial_services_committee),
    url(r'^switchers$', switchers),
    url(r'^no_no$', no_no),
    url(r'^yes_yes$', yes_yes),
    url(r'^register$', register),
    url(r'^login/$', user_login),
    url(r'^dashboard$', user_dashboard),
]