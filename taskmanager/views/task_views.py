from django.shortcuts import render, redirect
from taskmanager.models import CustomUser,Task
from django.contrib.auth.decorators import login_required


@login_required
def create_task(request):
    users = CustomUser.objects.filter(role="USER")  # or Role.USER if using enum
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        assigned_to_id = request.POST.get("assigned_to")

        # ✅ Only assign if value exists
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
            assigned_to=assigned_to,  # can be None
            created_by=request.user
        )
        return redirect("task_list")  # or wherever your success page is

    return render(request, "create_task.html", {"users": users})





