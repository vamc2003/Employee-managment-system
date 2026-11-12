
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.models import User
from employees.models import Department
from tasks.models import Task
from django.utils import timezone
from django.db.models import Count, Q

@login_required
def home(request):

    user = request.user
    

    # ADMIN DASHBOARD
    if user.is_superuser or user.role == 'ADMIN':

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
            'overdue_tasks': Task.objects.filter(
            due_date__lt=timezone.localdate()
            ).exclude(status='COMPLETED').count(),
        }

        return render(request, 'dashboard/home.html', context)

    # MANAGER DASHBOARD

    elif user.role == 'MANAGER':

        # 1. Get tasks assigned by this manager
        manager_tasks = Task.objects.filter(
            assigned_by=user
        ).select_related(
            'assigned_to'
        ).order_by('-created_at')

        # 2. Calculate employee workload
        employee_workload = User.objects.filter(
            role='EMPLOYEE',
            assigned_tasks__assigned_by=user
        ).annotate(

            total_tasks=Count(
                'assigned_tasks',
                filter=Q(assigned_tasks__assigned_by=user)
            ),

            pending_count=Count(
                'assigned_tasks',
                filter=Q(
                    assigned_tasks__assigned_by=user,
                    assigned_tasks__status='PENDING'
                )
            ),

            in_progress_count=Count(
                'assigned_tasks',
                filter=Q(
                    assigned_tasks__assigned_by=user,
                    assigned_tasks__status='IN_PROGRESS'
                )
            ),

            completed_count=Count(
                'assigned_tasks',
                filter=Q(
                    assigned_tasks__assigned_by=user,
                    assigned_tasks__status='COMPLETED'
                )
            )

        ).annotate(

            # 3. Calculate completion percentage
            completion_percentage=Case(
                When(
                    total_tasks__gt=0,
                    then=ExpressionWrapper(
                        F('completed_count') * 100.0 / F('total_tasks'),
                        output_field=FloatField()
                    )
                ),
                default=Value(0.0),
                output_field=FloatField()
            )

        ).distinct()

        # 4. Manager dashboard context
        context = {

            'total_tasks': manager_tasks.count(),

            'pending_tasks': manager_tasks.filter(
                status='PENDING'
            ).count(),

            'in_progress_tasks': manager_tasks.filter(
                status='IN_PROGRESS'
            ).count(),

            'completed_tasks': manager_tasks.filter(
                status='COMPLETED'
            ).count(),

            'overdue_tasks': manager_tasks.filter(
                due_date__lt=timezone.localdate()
            ).exclude(
                status='COMPLETED'
            ).count(),

            'recent_tasks': manager_tasks[:5],

            'employee_workload': employee_workload,

        }

        return render(
            request,
            'dashboard/manager_home.html',
            context
        )


    # EMPLOYEE DASHBOARD
    elif user.role == 'EMPLOYEE':

        employee_tasks = Task.objects.filter(
            assigned_to=user
        ).order_by('-created_at')

        context = {
            'total_tasks': employee_tasks.count(),
            'pending_tasks': employee_tasks.filter(status='PENDING').count(),
            'in_progress_tasks': employee_tasks.filter(status='IN_PROGRESS').count(),
            'completed_tasks': employee_tasks.filter(status='COMPLETED').count(),
            'recent_tasks': employee_tasks[:5],'overdue_tasks': employee_tasks.filter(
                due_date__lt=timezone.localdate()
            ).exclude(status='COMPLETED').count(),
        }

        return render(request, 'dashboard/employee_home.html', context)

    return render(request, 'dashboard/home.html', {})
