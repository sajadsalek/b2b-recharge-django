from django.db import models
from src.common.models import BaseModel
from django.db.models import F

class Wallet(BaseModel):
    remaining = models.DecimalField(max_digits=10, decimal_places=2)

    def increase(self, amount):
        Wallet.objects.filter(pk=self.pk).update(remaining=F("remaining") + amount)

    def decrease(self, amount):
        wallet = Wallet.objects.filter(pk=self.pk).update(remaining=F("remaining") + amount)

    def __str__(self):
        return f"Wallet with balance {self.remaining}"

    class Meta:
        db_table = "Wallet"
