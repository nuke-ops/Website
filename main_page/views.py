from django.shortcuts import render


def main(request):
    return render(request, "main/main.html")


def main_ss13(request):
    return render(request, "main/ss13.html")


def main_ss13_rules(request):
    return render(request, "main/rules.html")
