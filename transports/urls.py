from django.urls import path, re_path
from . import views

urlpatterns = [
    path('transports/', views.TransportViewsNoID),
    path('transports/<int:id>', views.TransportViews),
]