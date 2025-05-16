from django.shortcuts import render, redirect
from taskmanager.models import Role, CustomUser,AssignedUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password




@login_required
def admin_panel(request):
    if request.user.role not in [Role.ADMIN, Role.SUPERUSER]:
        return render(request, "login.html", {"error": "Not authorized"})
    if request.user.role == Role.ADMIN:
        # If the user is an admin, filter users to show only those assigned to them
        assigned_user_ids = AssignedUser.objects.filter(admin=request.user).values_list('user_id', flat=True)
        users = CustomUser.objects.filter(id__in=assigned_user_ids)
        return render(request, "adminpanel.html", {
        "users": users
    })
    users = CustomUser.objects.filter(role=Role.USER)
    admins = CustomUser.objects.filter(role__in=[Role.ADMIN])


    return render(request, "adminpanel.html", {
        "users": users,
        "admins": admins
    })


@login_required
def user_panel(request):
    if request.user.role != Role.USER:
        return render(request, "login.html", {"error": "Not authorized"})
    return render(request, "userpanel.html")


@login_required
def create_user_view(request):
    role = request.GET.get("role", Role.USER)  # default to USER

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        selected_role = request.POST.get("role")

        if username and password and selected_role:
            CustomUser.objects.create(
                username=username,
                password=make_password(password),
                role=selected_role
            )
            # Redirect back to the list based on role
            if selected_role == Role.ADMIN:
                return redirect('/adminpanel/')  # or a dedicated admin list URL
            else:
                return redirect('/adminpanel/?show=users')  # or user list URL

    return render(request, "create_user.html", {"role": role})


