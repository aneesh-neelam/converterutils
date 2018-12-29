from django.test import TestCase

from .models import Currency, ConversionRates


class CurrencyModelsTest(TestCase):
    def create_currencies(self):
        Currency.objects.create(code='USD', name='US Dollar', symbol='$')
        Currency.objects.create(code='INR', name='Indian Rupee', symbol='₹')
        Currency.objects.create(code='EUR', name='Euro', symbol='€')
        Currency.objects.create(code='GBP', name='Pound Sterling', symbol='£')

    def create_conversion_rates(self):
        ConversionRates.objects.create(currency_id='USD', base_currency_id='USD', exchange_rate=1.0)
        ConversionRates.objects.create(currency_id='INR', base_currency_id='USD', exchange_rate=0.014)
        ConversionRates.objects.create(currency_id='EUR', base_currency_id='USD', exchange_rate=1.14)
        ConversionRates.objects.create(currency_id='GBP', base_currency_id='USD', exchange_rate=1.27)
        ConversionRates.objects.create(currency_id='USD', base_currency_id='INR', exchange_rate=69.93)
        ConversionRates.objects.create(currency_id='INR', base_currency_id='INR', exchange_rate=1.0)
        ConversionRates.objects.create(currency_id='EUR', base_currency_id='INR', exchange_rate=79.98)
        ConversionRates.objects.create(currency_id='GBP', base_currency_id='INR', exchange_rate=88.86)

    def delete_conversion_rates(self):
        ConversionRates.objects.all().delete()

    def delete_currencies(self):
        Currency.objects.all().delete()

    def setUp(self):
        self.create_currencies()
        self.create_conversion_rates()

    def test_currency_models(self):
        # Test number of currencies in Database
        currencies = Currency.objects.all()
        self.assertEqual(currencies.count(), 4)

        # Test number of exchange rate entries in Database
        conversion_rates = ConversionRates.objects.all()
        self.assertEqual(conversion_rates.count(), 8)

        # Get Exchange rates for all currencies against USD
        exchange_rates_for_usd = ConversionRates.objects.filter(base_currency_id='USD')
        self.assertEqual(exchange_rates_for_usd.count(), 4)

        # Get Exchange rates for all currencies against INR
        exchange_rates_for_inr = ConversionRates.objects.filter(base_currency_id='INR')
        self.assertEqual(exchange_rates_for_inr.count(), 4)

    def tearDown(self):
        self.create_conversion_rates()
        self.delete_currencies()
