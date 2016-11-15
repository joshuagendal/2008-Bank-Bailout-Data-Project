from django.conf.urls import include, url
from django.contrib import admin
from bailout.views import index, data, links, member_search, financial_services_committee, switchers, no_no, yes_yes, register, user_login, user_dashboard, rating_page, user_logout, members_by_user_state, user_ratings, analyze, order_by_pac, explain_variables

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
    url(r'^logout/$', user_logout),
    url(r'^dashboard$', user_dashboard),
    url(r'^dashboard/(?P<identifier>\d+)$', rating_page), #change to r'^/rate/...
    url(r'^dashboard/(?P<state>\w+)$', members_by_user_state),
    url(r'^ratings/$', user_ratings),
    url(r'^analyze/$', analyze),
    url(r'^order_by_pac/$', order_by_pac),
    url(r'^explain_variables$', explain_variables)






     # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
]