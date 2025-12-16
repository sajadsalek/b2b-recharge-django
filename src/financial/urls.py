from django.urls import path

from .apis.refill import RefillApi
# from .apis.subscription import SubscribeApi, SubscribeDetailApi


app_name = "blog"
urlpatterns = [
        # path("subscribe/", SubscribeApi.as_view(), name="subscribe"),
        # path("subscribe/<str:email>", SubscribeDetailApi.as_view(), name="subscribe_detail"),
        path("refill-request/", RefillApi.as_view(), name="refill-request"),
        # path("post/<slug:slug>", PostDetailApi.as_view(), name="post_detail"),
        ]

