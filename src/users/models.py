from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from src.common.models import BaseModel
from src.financial.model.wallet import Wallet


# from src.common.models import BaseModel, BaseUserManager


# class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=150, unique=True)
#
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#
#     objects = BaseUserManager()
#
#     USERNAME_FIELD = "username"
#
#     def __str__(self):
#         return self.username
#
#     @property
#     def is_staff(self):
#         return self.is_admin


class CustomUser(AbstractUser):
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )  # بدون quote
