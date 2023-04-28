from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.
#https://docs.djangoproject.com/en/4.2/topics/auth/customizing/

# Manager Custom accounts
class MyAccountManager(BaseUserManager):

    #for create custom user
    def create_user(self, first_name, last_name, username, email, password = None):
        #check fill information
        if not email or not username:
            raise ValueError('Missing email or username')

        #overdrive
        user = self.model(
            email = self.normalize_email(email), #Normalizes email addresses by lowercasing the domain portion of the email address.
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        #Sets the user’s password to the given raw string, taking care of the password hashing.
        user.set_password(password)
        #save indb
        user.save(using=self._db)
        return user
    
    #for create custom superuser(admin) 
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        
        #permission
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True

        user.save(using=self._db)
        user.save()
        return user

            
    
#Custom for accounts
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

    #define accounts object using MyAccountsManager operation
    objects = MyAccountManager()

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
    