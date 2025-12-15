from django.db import models
from src.common.models import BaseModel


class Transaction(BaseModel):

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    TransactionDate = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    # ... other fields
    class Meta:
        db_table = "Transaction"