from django.shortcuts import render, redirect
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

# Create your views here.


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(
            request,
            "signUp.html",
            {"form": UserCreationForm},
        )
    else:
        if (
            request.POST["password1"]
            == request.POST["password2"]
        ):
            try:
                # register user
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )

                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(
                    request,
                    "signUp.html",
                    {
                        "form": UserCreationForm,
                        "error": "User already exists",
                    },
                )

        return render(
            request,
            "signUp.html",
            {
                "form": UserCreationForm,
                "error": "Password do not match",
            },
        )


def tasks(request):
    return render(request, "tasks.html")


def logoutSession(request):
    logout(request)
    return redirect("home")


def loginUser(request):
    if request.method == "GET":
        return render(
            request,
            "login.html",
            {
                "form": AuthenticationForm,
                "error": "User or password are incorrect",
            },
        )
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        print(request.POST)
        if user is None:
            return render(
                request,
                "login.html",
                {
                    "form": AuthenticationForm,
                    "error": "Username or password are incorrect",
                },
            )
        else:
            login(request, user)
            return redirect("tasks")
