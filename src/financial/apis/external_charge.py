from math import trunc

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from src.api.mixins import ApiAuthMixin
from src.financial.model.external_charge_request import ExternalChargeRequest
from src.financial.services.external_charge_request_service import external_charge_request_

from drf_spectacular.utils import extend_schema


class ExternalChargeApi(ApiAuthMixin, APIView):
    class ExternalChargeInputSerializer(serializers.Serializer):
        amount = serializers.DecimalField(decimal_places=2, max_digits=10)
        phone_number = serializers.CharField(max_length=11,required=True)


    class ExternalChargeOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ExternalChargeRequest
            fields = ("amount", "phone_number", "requesting_user")

    @extend_schema(
        request=ExternalChargeInputSerializer,
        responses=ExternalChargeOutputSerializer,
        tags=["External-Charge-Request"],
    )
    def post(self, request):
        serializer = self.ExternalChargeInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refill = external_charge_request_(
                amount=serializer.validated_data["amount"],
                phone_number=serializer.validated_data["phone_number"],
                user=request.user,
            )
        except Exception as ex:
            return Response(f"Database Error {ex}", status=status.HTTP_400_BAD_REQUEST)
        return Response(self.ExternalChargeOutputSerializer(refill, context={"request": request}).data)
