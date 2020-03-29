from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class AccountManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("email is needed")
        if not username:
            raise ValueError("uname is needed")

        user= self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,username,password):
        user=self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email=models.EmailField(verbose_name='E-mail', max_length=30, unique=True)
    username=models.CharField(verbose_name='Username', max_length=30, unique=True)
    last_login=models.DateTimeField(verbose_name='Last Login', auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD ='username'
    REQUIRED_FIELDS=['email']
    objects=AccountManager()
    def __str__(self):
        return self.username

    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self, app_lebel):
        return True

    