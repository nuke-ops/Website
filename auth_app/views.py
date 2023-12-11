from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm


def user_login(request):
    if request.user.is_authenticated:
        return redirect("main")

    initial_next = request.GET.get("next", "main")
    form = LoginForm(initial={"next": initial_next})

    if request.method == "POST":
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

    return render(request, "auth/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")
