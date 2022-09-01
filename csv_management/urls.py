from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('my_reservations/', views.my_reservations, name='my_reservations'),
    path('my_reservations/download', views.download_my_reservations, name='download_my_reservations')
]

urlpatterns += staticfiles_urlpatterns()
