from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from django.core.validators import MinLengthValidator
from src.users.models import CustomUser
from src.users.services import register
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema


class RegisterApi(APIView):
    class InputRegisterSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=255)
        password = serializers.CharField(validators=[MinLengthValidator(limit_value=3)])
        confirm_password = serializers.CharField(max_length=255)

        def validate_username(self, username):
            if CustomUser.objects.filter(username=username).exists():
                raise serializers.ValidationError("username Already Taken")
            return username

        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Please fill password and confirm password")

            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("confirm password is not equal to password")
            return data

    class OutPutRegisterSerializer(serializers.ModelSerializer):
        token = serializers.SerializerMethodField("get_token")

        class Meta:
            model = CustomUser
            fields = ("username", "token", "date_joined")

        def get_token(self, user):
            data = dict()
            token_class = RefreshToken

            refresh = token_class.for_user(user)

            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)

            return data

    @extend_schema(
        request=InputRegisterSerializer,
        responses=OutPutRegisterSerializer,
        tags=["Registration"],
    )
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = register(
                username=serializer.validated_data.get("username"),
                password=serializer.validated_data.get("password"),
            )
        except Exception as ex:
            return Response(f"Database Error {ex}", status=status.HTTP_400_BAD_REQUEST)
        return Response(self.OutPutRegisterSerializer(user, context={"request": request}).data)
