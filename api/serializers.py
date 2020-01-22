import logging

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Rate, TransferHistory

logger = logging.getLogger("api.serializers")


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id", "username", "password", "email", "balance", "currency")
        write_only_fields = ("password",)
        read_only_fields = ("id",)

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            balance=validated_data["balance"],
            currency=validated_data["currency"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = "__all__"
        validators = []

    def save(self):
        Rate.objects.update_or_create(
            currency_base_id=self.validated_data["currency_base"],
            currency_conversion_id=self.validated_data["currency_conversion"],
            defaults=self.validated_data,
        )


class MoneyTransferSerializer(serializers.Serializer):
    payee = serializers.SlugRelatedField(
        queryset=UserModel.objects.all(), many=False, slug_field="username"
    )
    transfer_sum = serializers.DecimalField(max_digits=12, decimal_places=2)


class TransferHistoryToSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    user_to = serializers.SerializerMethodField()

    class Meta:
        model = TransferHistory
        fields = ["datetime", "user_to", "transfer_sum", "status"]

    def get_user_to(self, obj):
        return obj.user_to.username


class TransferHistoryFromSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    user_from = serializers.SerializerMethodField()

    class Meta:
        model = TransferHistory
        fields = ["datetime", "user_from", "transfer_sum", "status"]

    def get_user_from(self, obj):
        return obj.user_from.username
