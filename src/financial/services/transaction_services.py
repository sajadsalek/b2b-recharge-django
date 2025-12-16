from decimal import Decimal

from django.db import transaction as db_transaction
from django.db.models import QuerySet
from django.utils import timezone

from src.financial.model.transaction import Transaction
from src.financial.model.wallet import Wallet


def create_transaction(*, wallet: Wallet, amount: Decimal, description=None) -> QuerySet[Transaction]:
    now = timezone.now()

    with db_transaction.atomic():
        transaction = Transaction.objects.create(
            wallet=wallet,
            amount=amount,
            description=description,
            created_at=now,
        )

        if amount < 0:
            wallet.decrease(amount)

        if amount > 0:
            wallet.increase(amount)

        return transaction