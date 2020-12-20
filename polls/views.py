from django.shortcuts import render

# Create your views here.
from django.http import Http404
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Question

from . import serializers


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

class HelloApiView(APIView):
    """ Test API view"""

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Return a list of APIView features"""

        an_apiview = [
            'Use HTTP methods as function (get, post, patch, put, delete)',
            "It is similat to a traditional Django view",
            'Give you the most control over your logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name"""

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = f'Hello {name}'

            return Response({'message':message})
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

class SensorApiView(APIView):
    """ Test API view"""

    # serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Return a list of APIView features"""

        an_apiview = [
            'Use HTTP methods as function (get, post, patch, put, delete)',
            "It is similat to a traditional Django view",
            'Give you the most control over your logic',
            'Is mapped manually to URLs'
        ]

        return Response({'time': 123456778, 'x': 1, 'y': 2, 'z': 3, 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name"""

        # serializer = serializers.HelloSerializer(data=request.data)

        
        time = request.data.get('time')
        x = request.data.get('x')
        y = request.data.get('y')
        z = request.data.get('z')

        message = f'time: {time}, x: {x}, y: {y}, z: {z}'
        print(f"[INFO] Received message: {message}")

        return Response({'message':message})
    
        