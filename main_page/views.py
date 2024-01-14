from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt


def main(request):
    return render(request, "main/main.html")


def main_ss13(request):
    return render(request, "main/ss13.html")


@xframe_options_exempt
def main_ss13_rules(request):
    return render(request, "main/rules.html")


@xframe_options_exempt
def main_ss13_motd(request):
    return render(request, "main/ss13_MOTD.html")
