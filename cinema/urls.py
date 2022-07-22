from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('currently-playing/', views.currently_playing, name='currently_playing')
]

urlpatterns += staticfiles_urlpatterns()


