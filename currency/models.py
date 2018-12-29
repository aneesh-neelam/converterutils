from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=5, primary_key=True, blank=False)
    name = models.CharField(max_length=20, blank=False)
    symbol = models.CharField(max_length=5)


class ConversionRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=False, db_index=True, related_name='%(class)s_currency')
    base_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=False, db_index=True, related_name='%(class)s_base_currency')
    exchange_rate = models.FloatField(default=1.0, blank=False, null=False)
    last_updated = models.DateTimeField(auto_now=True)
