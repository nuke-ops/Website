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
from django.contrib import admin
from django.urls import path
from main_page.views import main, main_ss13, main_ss13_rules
from dice.views import dice, get_dice_rolls, insert_dice_roll, dice_electron
from error_handlers.views import error_handler
from django.conf.urls import handler404, handler500

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", main, name="main"),
    path("ss13/", main_ss13, name="main_ss13"),
    path("ss13/rules/", main_ss13_rules, name="main_ss13_rules"),
    path("dice/", dice, name="dice"),
    path("dice/electron", dice_electron, name="dice_electron"),
    path("api/get_dice_rolls/", get_dice_rolls, name="get_dice_rolls"),
    path("api/insert_dice_roll/", insert_dice_roll, name="insert_dice_roll"),
]

handler400 = error_handler
handler403 = error_handler
handler404 = error_handler
handler500 = error_handler
