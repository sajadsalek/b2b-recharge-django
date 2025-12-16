from decimal import Decimal

from django.db import transaction
from django.core.exceptions import ValidationError

from src.financial.model.external_charge_request import ExternalChargeRequest
from src.financial.model.wallet import Wallet
from src.financial.services.transaction_services import create_transaction
from src.users.models import CustomUser


def external_charge_request_(*, amount: Decimal, phone_number: str, user: CustomUser) -> ExternalChargeRequest:
    with transaction.atomic():
        user_wallet = Wallet.objects.select_for_update().get(id=user.wallet.id)

        check = user_wallet.remaining - amount
        if check < Decimal("0.00"):
            raise ValidationError("wallet balance is insufficient")

        tr = create_transaction(wallet=user_wallet, amount=amount * -1, description="for charge phone number")

        external_charge_request = ExternalChargeRequest.objects.create(
            amount=amount, phone_number=phone_number, transaction=tr, requesting_user=user
        )
        return external_charge_request
