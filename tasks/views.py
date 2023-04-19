from django.shortcuts import (
    get_object_or_404,
    render,
    redirect,
)
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)
from django.contrib.auth.models import User
from django.contrib.auth import (
    login,
    logout,
    authenticate,
)
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task

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
    tasks = Task.objects.filter(user=request.user)
    return render(request, "tasks.html", {"tasks": tasks})


def tasks_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    print(task)
    return render(
        request, "task_detail.html", {"task": task}
    )


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


def create_task(request):
    if request.method == "GET":
        return render(
            request,
            "create_task.html",
            {"forms": TaskForm()},
        )
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except:
            return render(
                request,
                "create_task.html",
                {
                    "forms": TaskForm,
                    "error": "Please provide valid data",
                },
            )
