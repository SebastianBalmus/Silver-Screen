from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>', views.reservation_options, name='reservation'),
]

urlpatterns += staticfiles_urlpatterns()
