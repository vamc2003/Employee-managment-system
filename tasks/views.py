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

        if user.is_superuser or user.role == 'ADMIN':
            return Task.objects.select_related(
                'assigned_to', 'assigned_by'
            ).order_by('-created_at')

        if user.role == 'MANAGER':
            return Task.objects.filter(
                assigned_by=user
            ).select_related(
                'assigned_to', 'assigned_by'
            ).order_by('-created_at')

        return Task.objects.filter(
            assigned_to=user
        ).select_related(
            'assigned_to', 'assigned_by'
        ).order_by('-created_at')

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
