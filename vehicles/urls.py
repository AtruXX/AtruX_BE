from django.urls import path, re_path
from . import views

urlpatterns = [
    path('trucks/', views.TruckViews),
    path('trucks/<int:id>', views.GetTruck),
]