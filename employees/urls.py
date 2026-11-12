from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmployeeListView.as_view(), name='employee_list'),
    path('create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path(
    '<int:pk>/update/',
    views.EmployeeUpdateView.as_view(),
    name='employee_update'
),
path(
    '<int:pk>/delete/',
    views.EmployeeDeleteView.as_view(),
    name='employee_delete'
),
]