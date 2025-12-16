from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.mixins import ApiAuthMixin
from src.api.pagination import  get_paginated_response, LimitOffsetPagination, get_paginated_response_context
from src.financial.model.transaction import Transaction
from src.financial.selectors.transaction_selector import transaction_list


class TransactionApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        page = serializers.IntegerField(required=False, default=0)
        page_size = serializers.IntegerField(required=False, default=10)
    class InputSerializer(serializers.Serializer):
        ...

    class OutPutSerializer(serializers.ModelSerializer):

        class Meta:
            model = Transaction
            fields = ("amount", "description", "created_at")

    @extend_schema(
        parameters=[FilterSerializer],
        responses=OutPutSerializer,
        tags=["Transaction"],
    )
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        self.Pagination.limit = filters_serializer.data['page_size']
        self.Pagination.offset = filters_serializer.data['page']

        try:
            query = transaction_list(user=request.user)
        except Exception as ex:
            return Response(
                {"detail": "Filter Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.OutPutSerializer,
            queryset=query,
            request=request,
            view=self,
        )