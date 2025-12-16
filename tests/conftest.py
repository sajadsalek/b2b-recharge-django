import pytest
from decimal import Decimal
from src.financial.model.wallet import Wallet
from tests.factories import CustomUserFactory, CustomUserFactoryWithAmount


@pytest.fixture
def wallet():
    return Wallet.objects.create(remaining=Decimal("0.00"))


@pytest.fixture
def wallet_with_balance():
    return Wallet.objects.create(remaining=Decimal("100.00"))


@pytest.fixture
def user():
    return CustomUserFactory()

@pytest.fixture
def user1():
    return CustomUserFactory()

@pytest.fixture
def user_with_amount():
    return CustomUserFactoryWithAmount()
