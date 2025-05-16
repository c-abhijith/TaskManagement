from django.shortcuts import render, redirect,get_object_or_404
from taskmanager.models import Role, CustomUser,AssignedUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Count


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



@login_required
def custom_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login_page')  # Replace with your login URL name

@login_required
def assign_user(request):
    assigned_admins_data = (
        AssignedUser.objects.values('admin')
        .annotate(count=Count('user'))
    )
    assigned_admins = []
    for item in assigned_admins_data:
        try:
            admin_obj = CustomUser.objects.get(id=item['admin'])
            assigned_admins.append({
                'admin': admin_obj,
                'count': item['count']
            })
        except CustomUser.DoesNotExist:
            continue

    assigned_user_ids = AssignedUser.objects.values_list('user_id', flat=True)
    unassigned_users = CustomUser.objects.filter(role=Role.USER).exclude(id__in=assigned_user_ids)
    return render(request, "assign_user.html", {
        "assigned_admins": assigned_admins,
        "unassigned_users": unassigned_users
    })

@login_required
def assign_user_create(request):
    admins = CustomUser.objects.filter(role=Role.ADMIN)
    assigned_user_ids = AssignedUser.objects.values_list('user_id', flat=True)
    unassigned_users = CustomUser.objects.filter(role=Role.USER).exclude(id__in=assigned_user_ids)
    if request.method == "POST":
        admin_id = request.POST.get("admin")
        user_id = request.POST.get("user")

        if admin_id and user_id:
            AssignedUser.objects.create(
                admin_id=admin_id,
                user_id=user_id
            )
            return redirect('assign_user')
    return render(request, "create_assign_user.html", {
        "admins": admins,
        "unassigned_users": unassigned_users})

@login_required
def assign_user_detail(request, admin_id):
    admin = get_object_or_404(CustomUser, id=admin_id, role=Role.ADMIN)

    assigned_users = AssignedUser.objects.filter(admin=admin).select_related("user")

    return render(request, "assign_details.html", {
        "admin": admin,
        "assigned_users": assigned_users
    })


@login_required
def task_list(request):
    if request.user.role not in [Role.ADMIN, Role.SUPERUSER]:
        return render(request, "login.html", {"error": "Unauthorized access"})

    tasks = [
        {
            "title": "Design Homepage",
            "assigned_to": "user_alice",
            "status": "In Progress",
            "due_date": "2024-08-01",
        },
        {
            "title": "Fix Login Bug",
            "assigned_to": "user_bob",
            "status": "Pending",
            "due_date": "2024-08-03",
        },
        {
            "title": "Database Backup",
            "assigned_to": "user_sarah",
            "status": "Completed",
            "due_date": "2024-07-28",
        },
    ]

    return render(request, "task_details.html", {"tasks": tasks})