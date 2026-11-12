from django.shortcuts import render
from accounts.models import User
from employees.models import Department


def home(request):

    context = {
        'total_employees': User.objects.filter(
            role='EMPLOYEE'
        ).count(),

        'total_departments': Department.objects.count(),

        'total_managers': User.objects.filter(
            role='MANAGER'
        ).count(),

        'total_admins': User.objects.filter(
            role='ADMIN'
        ).count(),
    }

    return render(
        request,
        'dashboard/home.html',
        context
    )