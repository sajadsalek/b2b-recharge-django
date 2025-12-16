from decimal import Decimal

from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError

from src.financial.model.refill_request import RefillRequest
from src.financial.model.wallet import Wallet
from src.users.models import CustomUser
from src.financial.services.transaction_services import create_transaction


def create_refill_request(*, user: CustomUser, amount: Decimal) -> RefillRequest:
    with transaction.atomic():
        refill_request = RefillRequest.objects.create(
            amount=amount,
            customer=user,
        )
        return refill_request


def approve_refill_request(*, request_id) -> None:
    with transaction.atomic():
        refill_request = RefillRequest.objects.select_for_update(of=('self',)).get(id=request_id)

        if refill_request.status != RefillRequest.PENDING:
            raise ValidationError("Request already processed")

        wallet = Wallet.objects.select_for_update().get(id=refill_request.customer.wallet.id)
        tr = create_transaction(wallet=wallet, amount=refill_request.amount)

        refill_request.status = RefillRequest.APPROVED
        refill_request.updated_at = timezone.now()
        refill_request.transaction = tr
        refill_request.save(update_fields=["status", "updated_at", "transaction"])


def reject_refill_request(*, request_id) -> None:
    with transaction.atomic():
        refill = RefillRequest.objects.select_for_update().get(id=request_id)

        if refill.status != RefillRequest.PENDING:
            raise ValidationError("Request already processed")

        refill.status = RefillRequest.REJECTED
        refill.updated_at = timezone.now()
        refill.save(update_fields=["status", "updated_at"])
