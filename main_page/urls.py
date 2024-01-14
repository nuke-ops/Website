from django.urls import path
from .views import (
    main,
    main_ss13,
    main_ss13_rules,
    main_ss13_motd,
    main_ss13_motd_rules,
)


urlpatterns = [
    path("", main, name="main"),
    path("ss13/", main_ss13, name="main_ss13"),
    path("ss13/rules/", main_ss13_rules, name="main_ss13_rules"),
    path("ss13/motd/", main_ss13_motd, name="main_ss13_motd"),
    path("ss13/motd/rules/", main_ss13_motd_rules, name="main_ss13_motd_rules"),
]
