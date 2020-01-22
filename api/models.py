from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    """ Валюты """

    name = models.CharField("name", max_length=3, primary_key=True, null=False)

    def __str__(self):
        return self.name


class Rate(models.Model):
    """ Курсы валют """

    class Meta:
        unique_together = (("currency_base", "currency_conversion"),)

    currency_base = models.ForeignKey(
        Currency, related_name="base_currency_set", on_delete=models.CASCADE, null=False
    )
    currency_conversion = models.ForeignKey(
        Currency,
        related_name="conversion_currency_set",
        on_delete=models.CASCADE,
        null=False,
    )
    rate = models.DecimalField(
        "rate", max_digits=15, decimal_places=10, null=True, default=None
    )
    date = models.DateField("rate date")

    def __str__(self):
        return f"{self.currency_base.name}-{self.currency_conversion.name}:{self.rate}"


class User(AbstractUser):
    """ Пользователь системы """

    email = models.EmailField(_("email address"), blank=False, unique=True, null=False)
    balance = models.DecimalField(
        "balance", max_digits=12, decimal_places=2, null=False, blank=False
    )
    currency = models.ForeignKey(
        Currency, related_name="currencies", on_delete=models.CASCADE, null=False
    )

    def __str__(self):
        return f"{self.username}: {self.balance} {self.currency.name}"


class TransferHistory(models.Model):
    """ История переводов """

    class Statuses(models.TextChoices):
        IN_QUEUE = "IN QUEUE"
        COMPLETE = "COMPLETE"
        ERROR = "ERROR"

    id = models.AutoField(primary_key=True)
    user_from = models.ForeignKey(
        User, related_name="user_from_set", on_delete=models.CASCADE, null=False
    )
    user_to = models.ForeignKey(
        User, related_name="user_to_set", on_delete=models.CASCADE, null=False
    )
    datetime = models.DateTimeField("operation datetime", auto_now=True)
    transfer_sum = models.DecimalField(
        "sum", max_digits=12, decimal_places=2, null=False
    )
    status = models.CharField(
        max_length=10, choices=Statuses.choices, default=Statuses.IN_QUEUE
    )

    def __str__(self):
        return f"{self.user_from.username!r} to {self.user_to.username!r}: " \
               f"{self.transfer_sum} {self.user_from.currency.name} - {self.status}"
