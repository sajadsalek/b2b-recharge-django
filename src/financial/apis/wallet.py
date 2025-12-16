from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.mixins import ApiAuthMixin
from src.financial.model.wallet import Wallet
from src.financial.selectors.wallet_selector import get_wallet


class WalletApi(ApiAuthMixin, APIView):
    class WalletInputSerializer(serializers.Serializer):
        ...

    class WalletOutPutSerializer(serializers.ModelSerializer):

        class Meta:
            model = Wallet
            fields = ("remaining",)

    @extend_schema(
        request=WalletInputSerializer,
        responses=WalletOutPutSerializer,
        tags=["Wallet"],
    )
    def get(self, request):

        try:
            query = get_wallet(user=request.user)
        except Exception as ex:
            return Response(
                {"detail": "Filter Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.WalletOutPutSerializer(query)
        return Response(serializer.data)
