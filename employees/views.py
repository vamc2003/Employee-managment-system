from django.shortcuts import render

# Create your views here.
from accounts.models import User


from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import EmployeeForm
from django.views.generic import ListView,DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import (
    AdminRequiredMixin,
    ManagerOrAdminRequiredMixin,
)

import secrets

class EmployeeCreateView(AdminRequiredMixin, CreateView):

    model = User
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee_list')

    def form_valid(self, form):

        # Assign employee role
        form.instance.role = 'EMPLOYEE'

        # Generate a random temporary password
        temporary_password = secrets.token_urlsafe(32)

        # Store it securely as a Django password hash
        form.instance.set_password(temporary_password)

        return super().form_valid(form)




from django.views.generic import ListView
from accounts.models import User


class EmployeeListView(ListView):

    model = User

    template_name = 'employees/employee_list.html'

    context_object_name = 'employees'

    paginate_by = 10

    def get_queryset(self):

        queryset = User.objects.filter(
            role='EMPLOYEE'
        ).select_related('department')

        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(
                username__icontains=search
            ) | queryset.filter(
                employee_id__icontains=search
            ) | queryset.filter(
                email__icontains=search
            )

        return queryset.order_by('id')


class EmployeeDetailView(DetailView):

    model = User

    template_name = 'employees/employee_detail.html'

    context_object_name = 'employee'

    def get_queryset(self):
        return User.objects.filter(role='EMPLOYEE')


class EmployeeUpdateView(UpdateView):

    model = User

    form_class = EmployeeForm

    template_name = 'employees/employee_form.html'

    success_url = reverse_lazy('employee_list')

    def get_queryset(self):
        return User.objects.filter(role='EMPLOYEE')

class EmployeeDeleteView(DeleteView):

    model = User

    template_name = 'employees/employee_confirm_delete.html'

    success_url = reverse_lazy('employee_list')

    def get_queryset(self):
        return User.objects.filter(role='EMPLOYEE')

    
