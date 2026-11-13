
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin, ModelAdmin):

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'department',
        'is_active',
    )

    list_filter = (
        'role',
        'department',
        'is_active',
    )

    search_fields = (
        'username',
        'email',
        'employee_id',
    )

    # Fields displayed when editing an existing user
    fieldsets = UserAdmin.fieldsets + (
        ('Employee Information', {
            'fields': (
                'employee_id',
                'role',
                'phone_number',
                'department',
            )
        }),
    )

    # Fields displayed when creating a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Employee Information', {
            'fields': (
                'email',
                'first_name',
                'last_name',
                'employee_id',
                'role',
                'phone_number',
                'department',
            )
        }),
    )
