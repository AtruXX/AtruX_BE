"""
URL configuration for AtruX project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

url_version = 'api/v0.1/'

urlpatterns = [
    path(url_version + 'admin/', admin.site.urls),
    path(url_version, include('api.urls')),
    path(url_version + 'auth/', include('djoser.urls')),
    path(url_version + 'auth/', include('djoser.urls.authtoken')),
    path(url_version, include('accounts.urls')),
    path(url_version, include('vehicles.urls')),
    # path(url_version, include('transports.urls')),
]
