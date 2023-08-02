"""road_bible URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path

from django.views import View
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.urls import path, include
from pwa import views as pwa_views
from django.views.generic.base import TemplateView # new
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    path('admin/clearcache/', include('clearcache.urls')),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),  # new
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
    
    path('', TemplateView.as_view(template_name='home.html'), name='home'), # new
    path("save_progress/", views.save_user_progress, name="save_progress"),
    path("get_progress/", views.get_user_progress, name="get_progress"), 
    path('', include('pwa.urls')),
    path('dashboard/', views.my_view, name='dashboard'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("dashboard/Psalm100", TemplateView.as_view(template_name="Psalm100.html"), name="Psalm100"),
    path("dashboard/Psalm23", TemplateView.as_view(template_name="Psalm23.html"), name="Psalm23"),
    path("dashboard/vacation", TemplateView.as_view(template_name="vacation.html"), name="vacation"),
    path("dashboard/romans", TemplateView.as_view(template_name="romansroad.html"), name="romans"),
]
