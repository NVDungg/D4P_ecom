from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class Account(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    #mention required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    #change login by username to email
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email
    
    #https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#custom-users-and-django-contrib-admin
    def has_perm(self, perm, obj=None):
        ''' Returns True if the user has the named permission. 
        If obj is provided, the permission needs to be checked against 
        a specific object instance.:'''
        return self.is_admin
    
    def has_module_perms(self, app_label):
        '''Returns True if the user has permission to access models in the given app'''
        return True
    