from django.urls import path
from . import views

urlpatterns = [
    path('get_drivers/', views.GetDrivers),
    path('get_profile/', views.GetProfile),
    path('give_rating/', views.GiveRating),
]

