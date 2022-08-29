from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('subscribe', views.subscribe, name='subscribe'),
]

urlpatterns += staticfiles_urlpatterns()
