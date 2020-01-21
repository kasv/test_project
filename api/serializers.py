import logging

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Currency, Rate, User, TransferHistory

logger = logging.getLogger("api.serializers")


# class UserSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = "__all__"
#
#
# class CurrencySerializer(ModelSerializer):
#     class Meta:
#         model = Currency
#         fields = "__all__"


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


# class TransferHistorySerializer(ModelSerializer):
#     class Meta:
#         model = TransferHistory
#         fields = "__all__"
        # exclude = ["id", "user_to", "user_from"]
