from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('EMPLOYEE', 'Employee'),
    ]

    employee_id = models.CharField(max_length=20,unique=True,null=True,blank=True)

    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='EMPLOYEE')

    phone_number = models.CharField(max_length=15,blank=True,null=True)
    department = models.ForeignKey('employees.Department',on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='users'
)

    def __str__(self):
        return self.username

