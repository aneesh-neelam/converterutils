from django.shortcuts import HttpResponse


def api_number_system_v1(request):
    return HttpResponse('Number System API v1 Index page')


def api_number_system_v1_convert(request):
    return HttpResponse('Number System Convert API v1')

