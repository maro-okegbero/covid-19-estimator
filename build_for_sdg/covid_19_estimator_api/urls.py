from django.urls import path
from .views import *

urlpatterns = [
    path('api/v1/on-covid-19', estimator),
    path('api/v1/on-covid-19/xml', estimator_xml),
    path('api/v1/on-covid-19/logs', logs_text),
]
