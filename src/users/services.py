from decimal import Decimal
from django.db import transaction
from .models import CustomUser
from src.financial.models import Wallet


def create_user(*, username: str, password: str) -> CustomUser:
    return CustomUser.objects.create_user(username=username, password=password)


def register(*, username: str, password: str) -> CustomUser:
    with transaction.atomic():
        user = create_user(username=username, password=password)
        wallet = Wallet.objects.create(remaining=Decimal('0.00'))  # پیش‌فرض اعتبار 0
        user.wallet = wallet
        user.save(update_fields=['wallet'])
        return user