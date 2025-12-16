from django.db import models
from src.common.models import BaseModel
from src.financial.model.wallet import Wallet




class Transaction(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, null=True, blank=True)
    wallet = models.ForeignKey(
        Wallet,
        related_name="transactions",
        on_delete=models.PROTECT,
    )

    class Meta:
        db_table = "Transaction"