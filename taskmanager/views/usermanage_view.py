from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from taskmanager.models import Role
from django.contrib.auth.decorators import login_required


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("--------------1-")
        user = authenticate(request, username=username, password=password)
        print("---------------2",user)

        if user is not None:
            login(request, user)
            print("---------------",user.role)
            if user.role == Role.ADMIN or user.role == Role.SUPERUSER:
                print("---ok----")
                return redirect('/adminpanel/')
            elif user.role == Role.USER:
                return redirect('/userpanel/')
            else:
                return render(request, "login.html", {"error": "Unknown role!"})
        else:
            return render(request, "login.html", {"error": "Invalid credentials!"})
    else:
        return render(request, "login.html")
    # return render(request, "login.html")


    

@login_required
def admin_panel(request):
    if request.user.role not in [Role.ADMIN, Role.SUPERUSER]:
        return render(request, "login.html", {"error": "Not authorized"})
    return render(request, "adminpanel.html")


@login_required
def user_panel(request):
    if request.user.role != Role.USER:
        return render(request, "login.html", {"error": "Not authorized"})
    return render(request, "userpanel.html")