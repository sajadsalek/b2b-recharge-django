from src.financial.model.transaction import Transaction
from src.users.models import CustomUser


def transaction_list(*, user: CustomUser) -> list[Transaction]:
    transactions = list(Transaction.objects.filter(wallet=user.wallet).order_by("-created_at"))
    return transactions
