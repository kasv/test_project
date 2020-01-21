import logging

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import DjangoModelPermissions

from .models import Currency, Rate, User, TransferHistory
# from .serializers import (
#     CurrencySerializer,
#     RateSerializer,
#     UserSerializer,
#     TransferHistorySerializer,
# )

logger = logging.getLogger("api")


def response_invalid_data(serializer):
    return Response({"success": False, "errors": serializer.errors})


class MoneyTransferAPIView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [DjangoModelPermissions]

    def post(self, request):
        current_user = request.user
        # serializer = CurrencySerializer(data=request.data, many=True)
        #
        # if not serializer.is_valid():
        #     return response_invalid_data(serializer)
        #
        # for data in serializer.data:
        #     pass


class TransferHistoryAPIView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [DjangoModelPermissions]
    queryset = TransferHistory.objects.all()

    def get(self, request):
        current_user = request.user
        outgoing_payments = TransferHistory.objects.filter(
            user_from=current_user
        ).order_by("datetime")
        incoming_payments = TransferHistory.objects.filter(
            user_to=current_user
        ).order_by("datetime")

        return Response(
            {
                "success": True,
                "result": {
                    "incoming_payments": incoming_payments,
                    "outgoing_payments": outgoing_payments,
                },
            }
        )
