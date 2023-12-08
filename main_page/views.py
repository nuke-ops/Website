from django.shortcuts import render
from django.http import HttpResponse

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def main(request):
    return render(request, "main/main.html")


def main_ss13(request):
    return render(request, "main/ss13.html")


def main_ss13_rules(request):
    return render(request, "main/rules.html")
