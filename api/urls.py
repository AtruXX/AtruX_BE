from django.urls import path
from . import views

urlpatterns = [
    path('get_drivers/', views.GetDrivers)
]

