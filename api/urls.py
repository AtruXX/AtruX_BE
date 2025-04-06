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
    path("create_transport/", views.createTransport),
    path("upload_transport_documents/", views.UploadTransportDocuments),
    path('update_transport/', views.transportUpdate),
    path('delete_transport_document/', views.deleteTransportDocument),
    path('list_transports/', views.transportList),
    path('delete_transport/', views.transportDelete),
    path("upload-google-sheets/", upload_to_google_sheets, name="upload_google_sheets"),
    path('add_cmr/', views.addCMR),
    path('delete_cmr/', views.deleteCMR),
    path('update_cmr/', views.updateCMR),
    path("add_truck/", views.addTruck),
    path("get_cmrs/<int:transport_id>", views.getCMRByTransport),
    path("upload_truck_document/", views.UploadTruckDocuments), #todo
    path("delete_truck/", views.deleteTruck),
    path("get_trucks/", views.getAllTrucks),
    path("add_trailer/", views.addTrailer),
    path("delete_trailer/", views.deleteTrailer),
    path("get_trailers/", views.getAllTrailers),
    path("latest_n_transports/<int:n>/<int:driver_id>/", views.latestNTransports),
    path("cmr_exists/<int:transport_id>/", views.doesCMRExist),
]

