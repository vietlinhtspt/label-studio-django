from django.shortcuts import render

# Create your views here.
from django.http import Http404
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")