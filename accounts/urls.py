from django.urls import path
from .views import activation_page, reset_password_page, reset_pass_ok, activation_page_ok

urlpatterns = [
    path('activate/<str:uid>/<str:token>/', activation_page, name = 'activation'),
    path('password/reset/confirm/<str:uid>/<str:token>/', reset_password_page, name='passwordreset'),
    path('password/reset/confirm/ok', reset_pass_ok, name='passwordresetOK'),
    path('activate/email/ok', activation_page_ok, name='activationOK'),
]