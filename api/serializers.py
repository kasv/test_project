import logging

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Rate

logger = logging.getLogger("api.serializers")


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id", "username", "password", "email", "balance", "currency")
        extra_kwargs = {
            "balance": {"required": True},
            "currency": {"required": True},
            "email": {"required": True},
        }
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


class RateSerializer(ModelSerializer):
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
