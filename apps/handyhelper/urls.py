from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process_register/$', views.process_register),
    url(r'^process_login/$', views.process_login),
    url(r'^dashboard/$', views.dashboard),
    url(r'^logout/$', views.logout),
    url(r'^add_job/$', views.add_job),
    url(r'^process_add_job/$', views.process_add_job),
    url(r'^view/(?P<id>\d+)/$', views.view_job),
    url(r'^add/(?P<id>\d+)/$', views.add),
    url(r'^edit/(?P<id>\d+)/$', views.edit_job),
    url(r'^cancel/(?P<id>\d+)/$', views.cancel),
    url(r'^process_edit_job/(?P<id>\d+)/$', views.process_edit_job),
    url(r'^myjob_cancel/(?P<id>\d+)/$', views.myjob_cancel),
    url(r'^myjob_view/(?P<id>\d+)/$', views.myjob_view_job),
]