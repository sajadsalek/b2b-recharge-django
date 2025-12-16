from decimal import Decimal
import pytest

from src.financial.selectors.refill_request_selector import get_refill_request
from src.financial.selectors.transaction_selector import transaction_list
from src.financial.services.refill_request_service import (
    create_refill_request,
    approve_refill_request,
    reject_refill_request,
)
from src.financial.selectors.wallet_selector import get_wallet


@pytest.mark.django_db
def test_create_new_refill_request_and_approve(user):
    ref = create_refill_request(user=user, amount=Decimal("10"))
    wal = get_wallet(user=user)

    assert Decimal("0") == wal.remaining

    approve_refill_request(request_id=ref.id)
    wal1 = get_wallet(user=user)
    transaction = transaction_list(user=user)

    new_ref = get_refill_request(request_id=ref.id)

    assert 1 == len(transaction)
    assert wal1.remaining == transaction[0].amount
    assert ref.amount == wal1.remaining
    assert "Approved" == new_ref.status


@pytest.mark.django_db
def test_create_new_refill_request_and_reject(user):
    ref = create_refill_request(user=user, amount=Decimal("10"))
    wal = get_wallet(user=user)

    assert Decimal("0") == wal.remaining

    reject_refill_request(request_id=ref.id)
    wal1 = get_wallet(user=user)

    assert Decimal("0") == wal1.remaining
