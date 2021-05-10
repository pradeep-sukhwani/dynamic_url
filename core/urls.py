from django.urls import path, re_path
from rest_framework import routers

from . import views

app_name = 'core-app'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    re_path('^active_endpoints/$', views.ActiveEndpointsView.as_view(), name='active_endpoints'),
    re_path('^active_endpoint/(?P<endpoint>[\w-]+)', views.EndpointView.as_view(), name='active_endpoints'),
    # Here the URL expects endpoint or blank (if it is a post request)
    re_path(r'^add_update_endpoint/(?P<endpoint>[\w-]+)|/$', views.url_endpoint, name='endpoint'),
]
