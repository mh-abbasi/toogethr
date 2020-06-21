from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Main customized user model"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, default='No Name')
    last_name = models.CharField(max_length=255, default='No Last Name')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
