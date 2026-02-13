from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Currency, ConversionRate


@require_GET
def api_currency_v1(request):
    currencies = Currency.objects.all().values('code', 'name', 'symbol')
    return JsonResponse({'currencies': list(currencies)})


@require_GET
def api_currency_v1_convert(request):
    source = request.GET.get('from')
    target = request.GET.get('to')
    amount_str = request.GET.get('amount')

    if not source or not target or not amount_str:
        return JsonResponse(
            {'error': 'Missing required parameters: from, to, amount'},
            status=400,
        )

    try:
        amount = float(amount_str)
    except ValueError:
        return JsonResponse(
            {'error': 'Invalid amount: must be a number'},
            status=400,
        )

    try:
        conversion_rate = ConversionRate.objects.get(
            currency__code=source,
            base_currency__code=target,
        )
    except ConversionRate.DoesNotExist:
        return JsonResponse(
            {'error': 'No conversion rate found from {0} to {1}'.format(source, target)},
            status=404,
        )

    converted_amount = amount * conversion_rate.exchange_rate

    return JsonResponse({
        'from': source,
        'to': target,
        'amount': amount,
        'converted_amount': converted_amount,
        'exchange_rate': conversion_rate.exchange_rate,
    })
