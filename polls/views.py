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

import paho.mqtt.client as mqtt 
    
import json


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

    HOST_URL = "broker.emqx.io"
    HOST_PORT = 1883
    KEEP_ALIVE = 60 
    TOPIC = "linhnv/gyro/android/1"
    SAVED_LOGS_PATH = ""

    IS_RECORD = False
    """
    KEEP_ALIVE : Maximum period in seconds between communications with the
            broker. If no other messages are being exchanged, this controls the
            rate at which the client will send ping messages to the broker.
    """

    def __init__(self, topic="linhnv/gyro/android/1"):
        # initializing instance variable
        self.TOPIC=topic
        print(self.TOPIC)
        print("Inited")

    def on_connect(mqttc, obj, flags, rc):
        print("rc: "+str(rc))
        if rc==0:
            mqttc.connected_flag=True #set flag
            print("connected OK")
        else:
            print("Bad connection Returned code=",rc)
            mqttc.bad_connection_flag=True

        

    def on_message(mqttc, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def on_publish(mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(mqttc, obj, level, string):
        print(string)

    def on_disconnect(mqttc, userdata, rc):
        print("disconnecting reason  "  +str(rc))
        mqttc.connected_flag=False
        mqttc.disconnect_flag=True

    mqtt.Client.connected_flag=False
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.on_disconnect = on_disconnect
    print(mqttc.connect(HOST_URL,HOST_PORT,KEEP_ALIVE))
    print(mqttc.subscribe(TOPIC, 0))

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
        message = json.dumps(message)
        if not self.mqttc.connected_flag: #wait in loop
            self.mqttc.connect(self.HOST_URL, self.HOST_PORT, self.KEEP_ALIVE)
            self.mqttc.subscribe(self.TOPIC, 0)

        self.mqttc.publish(self.TOPIC,message)
        print(f"[INFO] Received message: {message}")

        return Response({'message':message, "is_connected":self.mqttc.connected_flag})

class SensorAccApiView(APIView):
    """ Test API view"""

    # serializer_class = serializers.HelloSerializer

    HOST_URL = "broker.emqx.io"
    HOST_PORT = 1883
    KEEP_ALIVE = 60 
    TOPIC = "linhnv/gyro/android/acc"
    SAVED_LOGS_PATH = ""

    IS_RECORD = False
    """
    KEEP_ALIVE : Maximum period in seconds between communications with the
            broker. If no other messages are being exchanged, this controls the
            rate at which the client will send ping messages to the broker.
    """

    def on_connect(mqttc, obj, flags, rc):
        print("rc: "+str(rc))
        if rc==0:
            mqttc.connected_flag=True #set flag
            print("connected OK")
        else:
            print("Bad connection Returned code=",rc)
            mqttc.bad_connection_flag=True

        

    def on_message(mqttc, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def on_publish(mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(mqttc, obj, level, string):
        print(string)

    def on_disconnect(mqttc, userdata, rc):
        print("disconnecting reason  "  +str(rc))
        mqttc.connected_flag=False
        mqttc.disconnect_flag=True

    mqtt.Client.connected_flag=False
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.on_disconnect = on_disconnect
    print(mqttc.connect(HOST_URL,HOST_PORT,KEEP_ALIVE))
    print(mqttc.subscribe(TOPIC, 0))

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
        message = json.dumps(message)
        if not self.mqttc.connected_flag: #wait in loop
            self.mqttc.connect(self.HOST_URL, self.HOST_PORT, self.KEEP_ALIVE)
            self.mqttc.subscribe(self.TOPIC, 0)

        self.mqttc.publish(self.TOPIC,message)
        print(f"[INFO] Received message: {message}")

        return Response({'message':message, "is_connected":self.mqttc.connected_flag})


class SensorGyroApiView(APIView):
    """ Test API view"""

    # serializer_class = serializers.HelloSerializer

    HOST_URL = "broker.emqx.io"
    HOST_PORT = 1883
    KEEP_ALIVE = 60 
    TOPIC = "linhnv/gyro/android/gyro"
    SAVED_LOGS_PATH = ""

    IS_RECORD = False
    """
    KEEP_ALIVE : Maximum period in seconds between communications with the
            broker. If no other messages are being exchanged, this controls the
            rate at which the client will send ping messages to the broker.
    """

    def on_connect(mqttc, obj, flags, rc):
        print("rc: "+str(rc))
        if rc==0:
            mqttc.connected_flag=True #set flag
            print("connected OK")
        else:
            print("Bad connection Returned code=",rc)
            mqttc.bad_connection_flag=True

        

    def on_message(mqttc, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def on_publish(mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(mqttc, obj, level, string):
        print(string)

    def on_disconnect(mqttc, userdata, rc):
        print("disconnecting reason  "  +str(rc))
        mqttc.connected_flag=False
        mqttc.disconnect_flag=True

    mqtt.Client.connected_flag=False
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.on_disconnect = on_disconnect
    print(mqttc.connect(HOST_URL,HOST_PORT,KEEP_ALIVE))
    print(mqttc.subscribe(TOPIC, 0))

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
        message = json.dumps(message)
        if not self.mqttc.connected_flag: #wait in loop
            self.mqttc.connect(self.HOST_URL, self.HOST_PORT, self.KEEP_ALIVE)
            self.mqttc.subscribe(self.TOPIC, 0)

        self.mqttc.publish(self.TOPIC,message)
        print(f"[INFO] Received message: {message}")

        return Response({'message':message, "is_connected":self.mqttc.connected_flag})        