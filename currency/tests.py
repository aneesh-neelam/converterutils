import json

from django.test import TestCase, Client

from .models import Currency, ConversionRate


class CurrencyModelsTest(TestCase):
    def create_currencies(self):
        Currency.objects.create(code='USD', name='US Dollar', symbol='$')
        Currency.objects.create(code='INR', name='Indian Rupee', symbol='₹')
        Currency.objects.create(code='EUR', name='Euro', symbol='€')
        Currency.objects.create(code='GBP', name='Pound Sterling', symbol='£')

    def create_conversion_rates(self):
        ConversionRate.objects.create(currency_id='USD', base_currency_id='USD', exchange_rate=1.0)
        ConversionRate.objects.create(currency_id='INR', base_currency_id='USD', exchange_rate=0.014)
        ConversionRate.objects.create(currency_id='EUR', base_currency_id='USD', exchange_rate=1.14)
        ConversionRate.objects.create(currency_id='GBP', base_currency_id='USD', exchange_rate=1.27)
        ConversionRate.objects.create(currency_id='USD', base_currency_id='INR', exchange_rate=69.93)
        ConversionRate.objects.create(currency_id='INR', base_currency_id='INR', exchange_rate=1.0)
        ConversionRate.objects.create(currency_id='EUR', base_currency_id='INR', exchange_rate=79.98)
        ConversionRate.objects.create(currency_id='GBP', base_currency_id='INR', exchange_rate=88.86)

    def delete_conversion_rates(self):
        ConversionRate.objects.all().delete()

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
        conversion_rates = ConversionRate.objects.all()
        self.assertEqual(conversion_rates.count(), 8)

        # Get Exchange rates for all currencies against USD
        exchange_rates_for_usd = ConversionRate.objects.filter(base_currency_id='USD')
        self.assertEqual(exchange_rates_for_usd.count(), 4)

        # Get Exchange rates for all currencies against INR
        exchange_rates_for_inr = ConversionRate.objects.filter(base_currency_id='INR')
        self.assertEqual(exchange_rates_for_inr.count(), 4)

    def tearDown(self):
        self.delete_conversion_rates()
        self.delete_currencies()


class CurrencyViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        Currency.objects.create(code='USD', name='US Dollar', symbol='$')
        Currency.objects.create(code='INR', name='Indian Rupee', symbol='₹')
        ConversionRate.objects.create(currency_id='USD', base_currency_id='INR', exchange_rate=69.93)
        ConversionRate.objects.create(currency_id='INR', base_currency_id='USD', exchange_rate=0.014)

    def test_currency_list(self):
        response = self.client.get('/api/v1/currency/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('currencies', data)
        self.assertEqual(len(data['currencies']), 2)

    def test_convert_success(self):
        response = self.client.get('/api/v1/currency/convert/', {
            'from': 'USD',
            'to': 'INR',
            'amount': '100',
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['from'], 'USD')
        self.assertEqual(data['to'], 'INR')
        self.assertEqual(data['amount'], 100.0)
        self.assertAlmostEqual(data['converted_amount'], 6993.0)
        self.assertEqual(data['exchange_rate'], 69.93)

    def test_convert_missing_params(self):
        response = self.client.get('/api/v1/currency/convert/')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_convert_invalid_amount(self):
        response = self.client.get('/api/v1/currency/convert/', {
            'from': 'USD',
            'to': 'INR',
            'amount': 'abc',
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_convert_unknown_pair(self):
        response = self.client.get('/api/v1/currency/convert/', {
            'from': 'USD',
            'to': 'EUR',
            'amount': '100',
        })
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_convert_only_allows_get(self):
        response = self.client.post('/api/v1/currency/convert/', {
            'from': 'USD',
            'to': 'INR',
            'amount': '100',
        })
        self.assertEqual(response.status_code, 405)

    def tearDown(self):
        ConversionRate.objects.all().delete()
        Currency.objects.all().delete()
