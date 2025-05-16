from django.shortcuts import render, redirect
from taskmanager.models import Role,Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages


def login_page(request):
    # If user is already logged in
    if request.user.is_authenticated:
        if request.user.role == Role.ADMIN or request.user.role == Role.SUPERUSER:
            return redirect('/adminpanel/')
        elif request.user.role == Role.USER:
            return redirect('/userpanel/')
        else:
            return render(request, "login.html", {"error": "Unknown role!"})

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role == Role.ADMIN or user.role == Role.SUPERUSER:
                return redirect('/adminpanel/')
            elif user.role == Role.USER:
                return redirect('/userpanel/')
            else:
                return render(request, "login.html", {"error": "Unknown role!"})
        else:
            return render(request, "login.html", {"error": "Invalid credentials!"})
    
    return render(request, "login.html")


@login_required
def custom_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login_page')  # Replace with your login URL name




@login_required
def task_list(request):
    if request.user.role not in [Role.ADMIN, Role.SUPERUSER]:
        return render(request, "login.html", {"error": "Unauthorized access"})

    tasks = Task.objects.all().select_related('assigned_to')

    return render(request, "task_details.html", {"tasks": tasks})

