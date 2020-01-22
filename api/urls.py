from django.urls import path

from api.views import MoneyTransferAPIView, TransferHistoryAPIView, CreateUserAPIView

urlpatterns = [
    path("register", CreateUserAPIView.as_view()),
    path("pay", MoneyTransferAPIView.as_view()),
    path("history", TransferHistoryAPIView.as_view()),
]
