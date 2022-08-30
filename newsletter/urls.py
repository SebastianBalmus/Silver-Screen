from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>', views.unsubscribe, name='unsubscribe'),
]

urlpatterns += staticfiles_urlpatterns()
