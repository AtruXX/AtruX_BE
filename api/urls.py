from django.urls import path
from . import views

urlpatterns = [
    path('dispachers/', views.GetData),
    path('add/', views.addItem)
]

