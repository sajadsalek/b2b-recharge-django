from django.urls import path

from .apis.external_charge import ExternalChargeApi
from .apis.refill import RefillApi
from .apis.transaction import TransactionApi
from .apis.wallet import WalletApi


app_name = "blog"
urlpatterns = [
    path("refill-request/", RefillApi.as_view(), name="refill-request"),
    path("external-charge-request/", ExternalChargeApi.as_view(), name="external-charge-request"),
    path("transaction/", TransactionApi.as_view(), name="transaction"),
    path("wallet/", WalletApi.as_view(), name="wallet"),
]
