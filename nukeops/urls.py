"""
URL configuration for nukeops project.

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
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from auth_app.views import user_login
from error_handlers.views import error_400, error_403, error_404, error_500

from .settings import MEDIA_ROOT
from .views import media_access

urlpatterns = [
    path("admin/login/", user_login),
    path("admin/", admin.site.urls),
    re_path(r"^media/(?P<path>.*)", media_access, name="media"),
    path("robots.txt", serve, {"document_root": MEDIA_ROOT, "path": "robots.txt"}),
    path("sitemap.xml", serve, {"document_root": MEDIA_ROOT, "path": "sitemap.xml"}),
    path("", include("main_page.urls")),
    path("", include("dice.urls")),
    path("", include("auth_app.urls")),
    path("", include("stream.urls")),
]

handler400 = error_400
handler403 = error_403
handler404 = error_404
handler500 = error_500
