import threading
from decimal import Decimal
import pytest
from django.db import connections
from src.financial.selectors.transaction_selector import transaction_list
from src.financial.selectors.wallet_selector import get_wallet
from src.financial.services.external_charge_request_service import external_charge_request_
from src.financial.services.refill_request_service import create_refill_request, approve_refill_request
from src.users.models import CustomUser


@pytest.mark.django_db(transaction=True)
def test_external_charge_request_with_threading(user_with_amount):
    AMOUNT = Decimal("60.00")
    results = []

    def withdraw():
        try:
            external_charge_request_(amount=AMOUNT, phone_number="09122222222", user=user_with_amount)
            results.append(True)
        except Exception:
            results.append(False)

    t1 = threading.Thread(target=withdraw)
    t2 = threading.Thread(target=withdraw)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    wallet = get_wallet(user=user_with_amount)
    transactions = transaction_list(user=user_with_amount)

    assert 1 == len(transactions)
    assert results.count(True) == 1
    assert wallet.remaining == Decimal("40.00")


@pytest.mark.django_db(transaction=True)
def test_external_charge_request_for_tow_user_with_threading(user, user1):

    def create_refill_and_approved(user: CustomUser):
        ref = create_refill_request(user=user, amount=Decimal("10"))
        approve_refill_request(request_id=ref.id)

        wal = get_wallet(user=user)
        transactions = transaction_list(user=user)

        _sum = sum(tr.amount for tr in transactions)
        assert wal.remaining == _sum

    for _ in range(10):
        create_refill_and_approved(user=user)
        create_refill_and_approved(user=user1)

    assert len(transaction_list(user=user)) == 10
    assert len(transaction_list(user=user1)) == 10

    AMOUNT = Decimal("1.00")
    THREADS = 4
    CALLS_PER_THREAD = 100

    results_user_1 = []
    results_user_2 = []


    def withdraw(u: CustomUser, results: list):
        for _ in range(CALLS_PER_THREAD):
            try:
                external_charge_request_(
                    amount=AMOUNT,
                    phone_number="09122222222",
                    user=u
                )
                results.append(True)
            except Exception:
                results.append(False)

        connections["default"].close()

    threads = []

    for _ in range(THREADS):
        threads.append(threading.Thread(
            target=withdraw,
            args=(user, results_user_1)
        ))
        threads.append(threading.Thread(
            target=withdraw,
            args=(user1, results_user_2)
        ))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    user.wallet.refresh_from_db()
    user1.wallet.refresh_from_db()

    success_1 = results_user_1.count(True)
    success_2 = results_user_2.count(True)

    assert len(results_user_1) == 400
    assert len(results_user_2) == 400

    assert success_1 == 100
    assert success_2 == 100

    tx_sum_1 = sum(tr.amount for tr in transaction_list(user=user))
    tx_sum_2 = sum(tr.amount for tr in transaction_list(user=user1))

    assert user.wallet.remaining == tx_sum_1
    assert 0 == user.wallet.remaining
    assert user1.wallet.remaining == tx_sum_2
    assert 0 == user1.wallet.remaining