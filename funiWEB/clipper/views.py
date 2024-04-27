from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.


def index(request):
    return render(request, 'clipper.html')


def ajaxData(request):
    print('ajaxData')
