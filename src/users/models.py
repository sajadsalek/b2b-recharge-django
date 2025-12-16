from django.db import models
from django.contrib.auth.models import AbstractUser
from src.financial.model.wallet import Wallet


class CustomUser(AbstractUser):
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
