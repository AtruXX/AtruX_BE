from django.urls import path, re_path
from .views import activation_page, reset_password_page, reset_pass_ok, activation_page_ok
from . import views

urlpatterns = [
    path('activate/<str:uid>/<str:token>/', activation_page, name = 'activation'),
    path('password/reset/confirm/<str:uid>/<str:token>/', reset_password_page, name='passwordreset'),
    path('password/reset/confirm/ok', reset_pass_ok, name='passwordresetOK'),
    path('activate/email/ok', activation_page_ok, name='activationOK'),
    
    ### API VIEWS ###
    path('drivers/', views.GetAllDrivers),
    path('drivers/<int:id>', views.GetDriver),
    path('profile/', views.GetProfile),
    path('rating/<int:id>', views.GiveRating),
    path('status/', views.ChangeStatus),
    path('personal-documents/', views.DocumentViews),
    re_path(r'^personal-documents/(?P<category>[^/]+)/$', views.DocumentViews),
    path('personal-documents/<int:id>', views.DocumentViews),
]