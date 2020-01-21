from django.urls import path

from api.views import MoneyTransferAPIView, TransferHistoryAPIView


urlpatterns = [
    path("pay", MoneyTransferAPIView.as_view()),
    path("history", TransferHistoryAPIView.as_view()),
]
