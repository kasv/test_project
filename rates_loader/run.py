"""
Загрузчик курсов валют (из табл Currency) в БД (табл Rate) с биржи exchangeratesapi.io
"""
import logging
import datetime
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "test_project.settings"

import django

django.setup()

import requests

from api.models import Currency
from api.serializers import RateSerializer

logger = logging.getLogger("rates_loader")

BROKER_URL = (
    "https://api.exchangeratesapi.io/latest?base={base_currency}&symbols={currencies}"
)

headers = {"content-type": "application/json"}


if __name__ == "__main__":
    currencies = Currency.objects.values_list("name", flat=True)

    for currency_name in currencies:
        other_currencies = set(currencies) - set([currency_name])

        url = BROKER_URL.format(
            base_currency=currency_name, currencies=",".join(other_currencies)
        )
        resp = requests.get(url)

        if not resp.ok:
            logger.critical(resp.reason)
            resp.raise_for_status()

        res_data = resp.json()
        if "error" in res_data:
            logger.error(res_data)
            continue

        date = datetime.datetime.strptime(res_data["date"], "%Y-%m-%d").date()
        req_currencies = res_data["rates"]

        for conv_currency, rate in req_currencies.items():
            rate_serializer = RateSerializer(
                data={
                    "currency_base": currency_name,
                    "currency_conversion": conv_currency,
                    "date": date,
                    "rate": rate,
                }
            )

            if not rate_serializer.is_valid():
                logger.error(rate_serializer.errors)
                raise Exception(rate_serializer.errors)  # TODO: fix type exception

            rate_serializer.save()
