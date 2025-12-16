from django.conf import settings
from django.db import models
from src.common.models import BaseModel


class ExternalChargeRequest(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=11)

    transaction = models.ForeignKey('Transaction',on_delete=models.CASCADE)
    requesting_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    class Meta:
        db_table = "ExternalChargeRequest"
        ordering = ['-created_at']