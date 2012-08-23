from django.conf import settings
from django.conf.urls import patterns

urlpatterns = patterns('',
    (r'^setcurrency/$', 'currencies.views.set_currency'),
)
