from django.urls import path

from .apis.external_charge import ExternalChargeApi
from .apis.refill import RefillApi
# from .apis.subscription import SubscribeApi, SubscribeDetailApi


app_name = "blog"
urlpatterns = [
        # path("subscribe/", SubscribeApi.as_view(), name="subscribe"),
        # path("subscribe/<str:email>", SubscribeDetailApi.as_view(), name="subscribe_detail"),
        path("refill-request/", RefillApi.as_view(), name="refill-request"),
        path("external-charge-request/", ExternalChargeApi.as_view(), name="external-charge-request"),
        # path("post/<slug:slug>", PostDetailApi.as_view(), name="post_detail"),
        ]

