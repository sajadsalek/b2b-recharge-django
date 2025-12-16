from django.db import models

from src.financial.model.transaction import Transaction
from src.users.models import CustomUser

from src.common.models import BaseModel


class RefillRequest(BaseModel):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        db_table = "RefillRequest"
