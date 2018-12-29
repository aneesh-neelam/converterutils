from django.contrib import admin

from .models import Currency, ConversionRates

admin.site.register(Currency)
admin.site.register(ConversionRates)
