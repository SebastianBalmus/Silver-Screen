from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>', views.reservation_options, name='reservation'),
    path('movie=<int:movie>/schedule=<int:schedule>', views.select_seats, name='select_seats'),
    path('confirm/<int:reservation>', views.confirm_reservation, name='confirm_reservation'),
    path('success/<str:group>', views.success, name='reservation_successful')
]

urlpatterns += staticfiles_urlpatterns()
