from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password = None):
        if not email:
            raise ValueError("User must have an email address")
        
        if not username:
            raise ValueError("User must have a username")
        
        user = self.model(
            email = self.normalize_email(email), # if you neter in capital letters, this will convert in small letters
            username = username,
            first_name = first_name,
            last_name = last_name
        )

        user.set_password(password) # inbuild method to set the passowrd 
        user.save(using= self._db)
        return user
    
    # method to create superuser
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique= True)
    email = models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = MyAccountManager() # telling accounts to use this classes details fromabove

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "account"

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj = None): # we must use this if we create customer user model
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True
                       
