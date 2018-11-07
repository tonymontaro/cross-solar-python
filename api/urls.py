"""API URLs."""
from django.conf.urls import url
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('', views.PanelViewSet)

urlpatterns = [
    url(r'^(?P<panelid>\d+)/analytics/?$', views.HourAnalyticsView.as_view()),
    url(r'^(?P<panelid>\d+)/analytics/day/?$',
        views.DayAnalyticsView.as_view()),
]

urlpatterns += router.urls
