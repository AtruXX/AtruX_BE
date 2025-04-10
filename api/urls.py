from django.urls import path, re_path
from . import views
from offerSite.views import upload_to_google_sheets

urlpatterns = [
    path('get_drivers/', views.GetDrivers),
    path('get_profile/', views.GetProfile),
    path('give_rating/', views.GiveRating),
    path('change_status/', views.ChangeStatus),
    path('upload_documents/', views.UploadUserDocuments),
    re_path(r'^get_documents(?:/(?P<category>[^/]+))?/$', views.GetUserDocumentsList),
    path('delete_documents/', views.DeleteUserDocument),
    path('change_title/', views.ChangeDocumentTitle),
    path('replace_document/', views.ReplaceDocument),
    path('create_route/', views.CreateRoute),
    path('get_routes/', views.GetRoutes),
    path('create_driver/', views.createDriver),
    path("drivers_number/", views.numOfDrivers),
    path("create_transport/", views.createTransport), #tested
    path("upload_transport_documents/", views.UploadTransportDocuments), #tested
    path('update_transport/', views.transportUpdate), #tested
    path('delete_transport_document/', views.deleteTransportDocument), #tested
    path('list_transports/', views.transportList), #tested
    path('delete_transport/', views.transportDelete),
    path("upload-google-sheets/", upload_to_google_sheets, name="upload_google_sheets"),
]

