from django.urls import path, re_path
from . import truck_views, trailer_views

urlpatterns = [
    path('trucks/', truck_views.TruckViewsNoID),
    path('trucks/<int:id>', truck_views.TruckViews),
    
    path('truck-documents/<int:id>', truck_views.DocumentViews),

    path('trailers/', trailer_views.TrailerViewsNoID),
    path('trailers/<int:id>', trailer_views.TrailerViews),
    
    path('trailer-documents/<int:id>', trailer_views.TrailerDocumentViews),
]