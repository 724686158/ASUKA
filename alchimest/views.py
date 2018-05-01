# from django.shortcuts import render
from django.http import HttpResponse
# from django.http import Http404
# from alchimest.models import Package


def index(request):

    return HttpResponse("Hello index")

