from django.urls import path
from . import views

urlpatterns = [
    path('get_drivers/', views.GetDrivers),
    path('get_profile/', views.GetProfile),
    path('give_rating/', views.GiveRating),
    path('change_status/', views.ChangeStatus),
    path('upload_documents/', views.UploadUserDocuments),
    path('get_documents/', views.GetUserDocumentsList),
    path('delete_documents/', views.DeleteUserDocument),
    path('change_title/', views.ChangeDocumentTitle),
    path('replace_document/', views.ReplaceDocument),
]

