from django.shortcuts import HttpResponse


def api_currency_v1(request):
    return HttpResponse("Currency API v1 Index page")


def api_currency_v1_convert(request):
    return HttpResponse("Currency Convert API v1")
