import logging

from django.contrib.auth import get_user_model
from django.core import serializers
from django.db import transaction, DatabaseError
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import DjangoModelPermissions

from .models import TransferHistory, Rate

from .serializers import UserSerializer, MoneyTransferSerializer, TransferHistoryToSerializer, \
    TransferHistoryFromSerializer

logger = logging.getLogger("api")

UserModel = get_user_model()


def response_invalid_data(serializer):
    return Response({"success": False, "errors": serializer.errors})


class CreateUserAPIView(CreateAPIView):
    model = UserModel
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return response_invalid_data(serializer)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {"success": True}, status=status.HTTP_201_CREATED, headers=headers
        )


class MoneyTransferAPIView(APIView):
    """ перевод средств между пользователями с конвертацией валют """
    authentication_classes = [BasicAuthentication]

    def post(self, request):
        current_user = request.user

        serializer = MoneyTransferSerializer(data=request.data)
        if not serializer.is_valid():
            return response_invalid_data(serializer)

        payee, transfer_sum = serializer.validated_data.values()

        if current_user.balance < transfer_sum:
            return Response(
                {
                    "success": False,
                    "errors": "Your balance is less than the transfer amount",
                }
            )

        if current_user.currency == payee.currency:
            rate = 1
        else:
            rate = Rate.objects.get(
                currency_base=current_user.currency, currency_conversion=payee.currency
            ).rate

        current_user_new_balance = current_user.balance - transfer_sum
        assert (
            not current_user_new_balance < 0
        ), f"New balance 'current_user' is less 0: {current_user_new_balance}"

        payee_new_balance = (rate * transfer_sum) + payee.balance
        assert (
            not payee_new_balance < 0
        ), f"New balance 'payee' is less 0: {payee_new_balance}"

        th_statuses = TransferHistory.Statuses

        # создадим историю транзакции
        trans_hist = TransferHistory.objects.create(
            user_from=current_user,
            user_to=payee,
            transfer_sum=transfer_sum,
            status=th_statuses.IN_QUEUE,
        )
        trans_hist.save()
        try:
            with transaction.atomic():
                current_user.balance = current_user_new_balance
                current_user.save()
                payee.balance = payee_new_balance
                payee.save()

        except DatabaseError as ex:
            logger.critical(ex)
            trans_hist.status = th_statuses.ERROR
        else:
            trans_hist.status = th_statuses.COMPLETE
        finally:
            trans_hist.save()

        return Response({"success": True})


class TransferHistoryAPIView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [DjangoModelPermissions]
    queryset = TransferHistory.objects.all()

    def get(self, request):
        current_user = request.user
        outgoing_payments = TransferHistory.objects.filter(
            user_from=current_user
        ).order_by("-datetime")
        incoming_payments = TransferHistory.objects.filter(
            user_to=current_user
        ).order_by("-datetime")

        incoming_payments_serializer = TransferHistoryToSerializer(incoming_payments, many=True)
        outgoing_payments_serializer = TransferHistoryFromSerializer(outgoing_payments, many=True)

        return Response(
            {
                "success": True,
                "result": {
                    "incoming_payments": incoming_payments_serializer.data,
                    "outgoing_payments": outgoing_payments_serializer.data,
                },
            }
        )
