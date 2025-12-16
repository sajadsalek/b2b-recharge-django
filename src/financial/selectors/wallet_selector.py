from src.financial.model.wallet import Wallet
from src.users.models import CustomUser


def get_wallet(user:CustomUser) -> Wallet:
    return Wallet.objects.get(id=user.wallet.id)