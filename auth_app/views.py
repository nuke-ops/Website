import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm

TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


def verify_turnstile(token, ip=None):
    data = {
        "secret": settings.CLOUDFLARE_TURNSTILE_SECRET_KEY,
        "response": token,
    }
    if ip:
        data["remoteip"] = ip

    r = requests.post(TURNSTILE_VERIFY_URL, data=data, timeout=5)
    return r.json()


def user_login(request):
    if request.user.is_authenticated:
        return redirect("main")

    initial_next = request.GET.get("next", "main")
    form = LoginForm(initial={"next": initial_next})

    if request.method == "POST":
        # cf turnstile
        token = request.POST.get("cf-turnstile-response")
        if not token:
            messages.error(request, "Captcha missing.")
            return redirect("login")
        result = verify_turnstile(token, request.META.get("REMOTE_ADDR"))
        if not result.get("success"):
            messages.error(request, "Captcha failed. Try again.")

        # auth
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = form.cleaned_data.get("next", "main")
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")

    return render(
        request,
        "auth/login.html",
        {"form": form, "TURNSTILE_SITE_KEY": settings.CLOUDFLARE_TURNSTILE_SITE_KEY},
    )


def user_logout(request):
    logout(request)
    return redirect("login")
