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
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.urls import path, include
from pwa import views as pwa_views
from django.views.generic.base import TemplateView  # new
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from accounts.views import ResetPasswordView
app_name = 'road_bible'

urlpatterns = [

    path('admin/clearcache/', include('clearcache.urls')),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),  # new
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),





    path('api/settings/', views.settings, name='settings'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),  # new
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

    path('serviceworker.js', TemplateView.as_view(template_name='serviceworker.js',
         content_type='application/javascript'), name='service-worker'),
    path('OneSignalSDKWorker.js', TemplateView.as_view(
        template_name='OneSignalSDKWorker.js', content_type='application/javascript')),
    path('', include('pwa.urls')),
    path('dashboard/', views.my_view, name='dashboard'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("roads/vacation",
         TemplateView.as_view(template_name="vacation.html"), name="vacation"),
    path('restore_progress/', views.restore_progress, name='restore_progress'),
    path("roads/Versestoliveby",
         TemplateView.as_view(template_name="Versestoliveby.html"), name="Versestoliveby"),
    path("api/save_progress/", views.save_progress, name='save_progress'),
    path('betatesters/', TemplateView.as_view(template_name="betatesters.html"),
         name='betatesters'),
    path("makeroad", TemplateView.as_view(
        template_name="makeroad.html"), name="makeroad"),
    path("418", TemplateView.as_view(template_name="418.html"), name="418"),
    path("roadmap", TemplateView.as_view(
        template_name="roadmap.html"), name="roadmap"),
    path("roads/chromecast",
         TemplateView.as_view(template_name="chromecast.html"), name="chromecast"),
    path("requestroad", TemplateView.as_view(
        template_name="requestroad.html"), name="requestroad"),
    path('roads/<str:group_name>/', views.verses_view, name='verses_view'),
    path('api/get_saved_progress/', views.get_saved_progress,
         name='get_saved_progress'),
    path("demo", TemplateView.as_view(template_name="demo.html"), name="demo"),
    path('roads/eli/<str:group_name>/',
         views.verses_eli_view, name='verses_eli_view'),
    path('share/<str:road>/<str:creator>/', views.share_road),
    path('userdash/', views.user_dash, name='userdash'),
    path('api/delete/', views.delete, name='delete'),
    path('api/approve/', views.approve, name="approve"),
    path('api/getroad/', views.getroads, name='getroad'),
    path('api/newroad/', views.save_verses, name='newroad'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/gameify/', views.gameify, name='gameify'),
    path('api/newfav/', views.newfavorites, name="newfav"),
    path('api/getfav/', views.getfavorites, name="getfav"),
    path('api/pdf/', views.pdf, name='pdf'),
    path('api/newfriend/', views.newfriend, name='freindnew'),
    path('api/friends/', views.getfrienddata, name="getfr"),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
