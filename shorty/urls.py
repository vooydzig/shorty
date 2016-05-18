from django.conf.urls import url
from trimurl.views import index, redirect, details

urlpatterns = [
    url(r'!(?P<url>[A-Za-z0-9]+)$', details),
    url(r'(?P<url>[A-Za-z0-9]+)$', redirect),
    url(r'$', index),
]
