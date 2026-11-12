from django.shortcuts import render


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views.generic import DeleteView
from .models import Task
from .forms import TaskForm, TaskStatusForm
from accounts.mixins import (
    ManagerOrAdminRequiredMixin,
    RoleRequiredMixin,
)
from django.utils import timezone
from django.db.models import Q



class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def test_func(self):
        return (
            self.request.user.is_superuser
            or self.request.user.role in ['ADMIN', 'MANAGER']
        )

    def form_valid(self, form):
        form.instance.assigned_by = self.request.user
        return super().form_valid(form)
class TaskListView(LoginRequiredMixin, ListView):

    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10


    def get_queryset(self):
        user = self.request.user

            # Filter tasks based on user role
        if user.is_superuser or user.role == 'ADMIN':
            queryset = Task.objects.all()

        elif user.role == 'MANAGER':
            queryset = Task.objects.filter(assigned_by=user)

        else:
            queryset = Task.objects.filter(assigned_to=user)

        queryset = queryset.select_related('assigned_to', 'assigned_by')

            # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Filter by priority
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)

        # Filter overdue tasks
        overdue = self.request.GET.get('overdue')
        if overdue == '1':
            queryset = queryset.filter(
                due_date__lt=timezone.localdate()
            ).exclude(status='COMPLETED')
        # Search by task title or description
        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset.order_by('-created_at')


class TaskDetailView(LoginRequiredMixin, DetailView):

    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.role == 'ADMIN':
            return Task.objects.all()

        if user.role == 'MANAGER':
            return Task.objects.filter(assigned_by=user)

        return Task.objects.filter(assigned_to=user)

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def test_func(self):
        return (
            self.request.user.is_superuser
            or self.request.user.role in ['ADMIN', 'MANAGER']
        )

class TaskStatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Task
    form_class = TaskStatusForm
    template_name = 'tasks/task_status_form.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.role in ['ADMIN', 'MANAGER']:
            return Task.objects.all()

        if user.role == 'EMPLOYEE':
            return Task.objects.filter(assigned_to=user)

        return Task.objects.none()

    def test_func(self):
        user = self.request.user

        return (
            user.is_superuser
            or user.role in ['ADMIN', 'MANAGER', 'EMPLOYEE']
        )
