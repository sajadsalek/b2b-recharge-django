from django.db import models
from src.common.models import BaseModel

class Wallet(BaseModel):
    remaining = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = "Wallet"