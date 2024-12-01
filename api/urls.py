from django.urls import path
from . import views

urlpatterns = [
    path('get_drivers/', views.GetDrivers),
    path('get_profile/', views.GetProfile),
    path('give_rating/', views.GiveRating),
    path('change_status/', views.ChangeStatus),
    path('upload_documents/', views.UploadDriverDocument),
    path('get_documents/', views.GetDriverDocument),
]

