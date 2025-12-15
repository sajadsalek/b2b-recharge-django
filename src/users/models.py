from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from src.common.models import BaseModel, BaseUserManager




class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin
