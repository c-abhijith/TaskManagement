from django.shortcuts import render, redirect
from taskmanager.models import CustomUser,Task
from django.contrib.auth.decorators import login_required
from taskmanager.models import Role,Task,AssignedUser




@login_required
def task_list(request):
    if request.user.role not in [Role.ADMIN, Role.SUPERUSER]:
        return render(request, "login.html", {"error": "Unauthorized access"})

    tasks = Task.objects.all().select_related('assigned_to')

    return render(request, "task_details.html", {"tasks": tasks})



@login_required
def create_task(request):
    assigned_users = AssignedUser.objects.filter(admin=request.user).values_list('user', flat=True)
    users = CustomUser.objects.filter(id__in=assigned_users, role="USER") 
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        assigned_to_id = request.POST.get("assigned_to")
        assigned_to = None
        if assigned_to_id:
            try:
                assigned_to = CustomUser.objects.get(id=assigned_to_id)
            except CustomUser.DoesNotExist:
                assigned_to = None

        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            assigned_to=assigned_to,  
            created_by=request.user
        )
        return redirect("task_list")  

    return render(request, "create_task.html", {"users": users})





