from django.contrib import admin
from .models import Payment
from .forms import PaymentForm


class PaymentAdmin(admin.ModelAdmin):
    form = PaymentForm


# admin.py faylida Payment modelini ro'yxatga oling
admin.site.register(Payment, PaymentAdmin)
