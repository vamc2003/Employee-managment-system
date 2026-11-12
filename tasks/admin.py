
from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'assigned_to',
        'assigned_by',
        'priority',
        'status',
        'due_date',
    )

    list_filter = ('priority', 'status', 'due_date')

    search_fields = (
        'title',
        'assigned_to__username',
        'assigned_by__username',
    )

    ordering = ('due_date',)
