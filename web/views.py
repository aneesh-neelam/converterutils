from django.shortcuts import render, HttpResponse


def index(request):
    return HttpResponse("Web Index page")


def api(request):
    return HttpResponse("API Index page")


def api_v1(request):
    return HttpResponse("API v1 Index page")
