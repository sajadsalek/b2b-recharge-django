from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from src.api.mixins import ApiAuthMixin
from src.financial.model.refill_request import RefillRequest
from src.financial.services.refill_request_service import create_refill_request

from drf_spectacular.utils import extend_schema


class RefillApi(ApiAuthMixin, APIView):
    class RefillInputSerializer(serializers.Serializer):
        amount = serializers.DecimalField(decimal_places=2, max_digits=10)


    class RefillOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = RefillRequest
            fields = ("amount", "user", "status")

    @extend_schema(
        request=RefillInputSerializer,
        responses=RefillOutputSerializer,
        tags=["Refill-Request"],
    )
    def post(self, request):
        serializer = self.RefillInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refill = create_refill_request(
                user=request.user,
                amount=serializer.validated_data["amount"],
            )
        except Exception as ex:
            return Response(f"Database Error {ex}", status=status.HTTP_400_BAD_REQUEST)
        return Response(self.RefillOutputSerializer(refill, context={"request": request}).data)
