"""Cross-Solar URLs"""
from django.urls import include
from django.conf.urls import url


urlpatterns = [
    url(r'^panel/', include('api.urls')),
]
