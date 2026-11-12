from django.shortcuts import render
from accounts.models import User
from employees.models import Department
from tasks.models import Task
from django.contrib.auth.decorators import login_required
@login_required

def home(request):

    context = {
        'total_employees': User.objects.filter(role='EMPLOYEE').count(),
        'total_departments': Department.objects.count(),
        'total_managers': User.objects.filter(role='MANAGER').count(),
        'total_admins': User.objects.filter(role='ADMIN').count(),

        # Task Statistics
        'total_tasks': Task.objects.count(),

        'pending_tasks': Task.objects.filter(
            status='PENDING'
        ).count(),

        'in_progress_tasks': Task.objects.filter(
            status='IN_PROGRESS'
        ).count(),

        'completed_tasks': Task.objects.filter(
            status='COMPLETED'
        ).count(),
    }

    return render(request, 'dashboard/home.html', context)
