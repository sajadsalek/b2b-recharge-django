from decimal import Decimal
import threading
import pytest
from src.financial.selectors.wallet_selector import get_wallet
from src.financial.services.transaction_services import create_transaction
from tests.conftest import wallet
from django.db import connections
import decimal



@pytest.mark.django_db
def test_transaction_creates_and_updates_wallet(wallet_with_balance):
    amount = Decimal("25.00")

    tx = create_transaction(wallet=wallet_with_balance, amount=amount, description="test recharge")

    wallet_with_balance.refresh_from_db()

    assert tx.amount == amount
    assert wallet_with_balance.remaining == Decimal("125.00")


@pytest.mark.django_db(transaction=True)
def test_concurrent_updates(wallet):
    THREADS = 10
    ROUNDS = 10
    AMOUNT = Decimal("10.00")

    def worker():
        for _ in range(ROUNDS):
            create_transaction(wallet=wallet, amount=AMOUNT, description="test")
        connections["default"].close()

    threads = [threading.Thread(target=worker) for _ in range(THREADS)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    wallet.refresh_from_db()
    assert wallet.remaining == AMOUNT * THREADS * ROUNDS
