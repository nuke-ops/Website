from django.urls import path
from .views import main, main_ss13, main_ss13_rules, main_ss13_motd


urlpatterns = [
    path("", main, name="main"),
    path("ss13/", main_ss13, name="main_ss13"),
    path("ss13/rules/", main_ss13_rules, name="main_ss13_rules"),
    path("ss13/motd/", main_ss13_motd, name="main_ss13_motd"),
]
