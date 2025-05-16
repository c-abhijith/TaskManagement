from django.shortcuts import render, redirect,get_object_or_404
from taskmanager.models import Role, CustomUser,AssignedUser,Task
from django.contrib.auth.decorators import login_required
from django.db.models import Count




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
def change_assigned_user(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)
        user_id = request.POST.get("assigned_to")
        task.assigned_to = CustomUser.objects.get(id=user_id) if user_id else None
        task.save()
    return redirect('task_list')



@login_required
def task_assign_user(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user.role != Role.ADMIN:
        return redirect('task_list')

    assigned_user_ids = AssignedUser.objects.filter(admin=request.user).values_list('user_id', flat=True)
    users = CustomUser.objects.filter(id__in=assigned_user_ids)

    if request.method == "POST":
        new_user_id = request.POST.get("assigned_to")
        if new_user_id:
            task.assigned_to_id = new_user_id
        else:
            task.assigned_to = None
        task.save()
        return redirect('task_list')  

    return render(request, "update_task_assignment.html", {
        "task": task,
        "users": users,
    })


@login_required
def remove_user_in_admin(request, assignment_id):
    assignment = get_object_or_404(AssignedUser, id=assignment_id)

    if request.method == "POST":
        assignment.delete()
        return redirect('assign_user_detail', admin_id=assignment.admin.id)
