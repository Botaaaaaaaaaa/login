from ctypes.wintypes import HANDLE
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse("Hello User")


def about(request) -> HttpResponse:
    return HttpResponse("About Page")
