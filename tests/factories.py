import factory
from factory.django import DjangoModelFactory
from decimal import Decimal
from django.contrib.auth import get_user_model  # noqa
from src.financial.model.wallet import Wallet
from src.users.models import CustomUser


class WalletFactory(DjangoModelFactory):
    """
    Factory for Wallet model
    """

    class Meta:
        model = Wallet

    remaining = Decimal("0.00")


class WalletFactoryWithAmount(DjangoModelFactory):
    """
    Factory for Wallet model
    """

    class Meta:
        model = Wallet

    remaining = Decimal("100.00")


User = get_user_model()


class CustomUserFactory(DjangoModelFactory):
    """
    Factory for CustomUser with Wallet
    """

    class Meta:
        model = CustomUser
        django_get_or_create = ("username",)
        skip_postgeneration_save = True


    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")

    is_active = True
    is_staff = False
    is_superuser = False

    # اتصال کاربر به کیف پول
    wallet = factory.SubFactory(WalletFactory)

    password = factory.PostGenerationMethodCall("set_password", "123456")


class CustomUserFactoryWithAmount(DjangoModelFactory):
    """
    Factory for CustomUser with Wallet
    """

    class Meta:
        model = CustomUser
        django_get_or_create = ("username",)
        skip_postgeneration_save = True


    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")

    is_active = True
    is_staff = False
    is_superuser = False

    # اتصال کاربر به کیف پول
    wallet = factory.SubFactory(WalletFactoryWithAmount)

    password = factory.PostGenerationMethodCall("set_password", "123456")
