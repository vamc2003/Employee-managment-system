
from django import forms
from .models import Task
from accounts.models import User


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        fields = [
            'title',
            'description',
            'assigned_to',
            'priority',
            'status',
            'due_date',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task title'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter task description'
            }),

            'assigned_to': forms.Select(attrs={
                'class': 'form-select'
            }),

            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),

            'status': forms.Select(attrs={
                'class': 'form-select'
            }),

            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['assigned_to'].queryset = User.objects.filter(
            role='EMPLOYEE'
        )

class TaskStatusForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['status']

        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
