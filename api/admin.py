from django.contrib import admin

from .models import Currency, Rate, TransferHistory, User


admin.site.register(User)
admin.site.register(Currency)
admin.site.register(Rate)
admin.site.register(TransferHistory)
