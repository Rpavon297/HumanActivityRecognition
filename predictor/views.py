import numpy as np
import SimplifiedHAR as harnet
import matlab

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db.models.signals import post_save
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from predictor.models import SensorData, CurrentActivity
from predictor.serializers import SensorDataSerializer

session = {}


def start_up():
    print('Initializing neural network...')
    session['handle'] = harnet.initialize()


def index(request):
    sensordata = SensorData.objects.all()
    data = SensorDataSerializer(sensordata, many=True).data
    classes = [];

    for point in data:
        if point['activity'] not in classes:
            classes.append(point['activity']);

    context = {
        'data': len(data),
        'classes': classes
    }
    return render(request, 'index.html', context=context)


def prediction(request):
    prediction = CurrentActivity.objects.all()

    context = {
        'prediction': prediction
    }

    return render(request, 'prediction.html', context=context)


def lstm(data):
    # return session['handle'].predict(data.tolist())
    list = data.tolist()

    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            list[i][j] = float(list[i][j])

    session['handle'].predict(matlab.double(list))
    return "hey"


class MakePrediction(APIView):
    error = False
    response = ""
    handle = None

    def post(self, request):
        try:
            package = request.data['captures']
            X = []

            for sensorCapture in package:
                row = []
                for item in sensorCapture:
                    row.append(sensorCapture[item])
                X.append(row)
            X = np.transpose(X)

            self.response = lstm(X)

            # current_activity = CurrentActivity.objects.get_or_create(device_key=request.data['device_key'])
            # current_activity.activity = self.response
            # current_activity.save()
        except Exception as e:
            self.error = True
        return Response({
            'response': self.response,
            'error': self.error
        })


class AddData(APIView):
    error = False
    response = ""

    def post(self, request):
        try:
            package = request.data['captures']
            sequence = request.data['sequence']
            activity = request.data['activity']

            for sensorCapture in package:
                data = SensorData(accelx=sensorCapture['accelx'],
                                  accely=sensorCapture['accely'],
                                  accelz=sensorCapture['accelz'],
                                  gyrox=sensorCapture['gyrox'],
                                  gyroy=sensorCapture['gyroy'],
                                  gyroz=sensorCapture['gyroz'],
                                  orientx=sensorCapture['orientx'],
                                  orienty=sensorCapture['orienty'],
                                  orientz=sensorCapture['orientz'],
                                  instant=sensorCapture['instant'],
                                  activity=activity,
                                  sequence=sequence)
                data.save()

        except Exception as e:
            self.error = True

        return Response({
            'response': self.response,
            'error': self.error
        })


class GetDataset(APIView):
    error = False
    response = ""

    def get(self, request):
        try:
            data = SensorData.objects.all()
            captures = SensorDataSerializer(data, many=True).data

            classified = {}
            for capture in captures:
                classified.setdefault(capture['activity'], []).append(capture)

            self.response = classified

        except Exception as e:
            self.error = True

        return Response({
            'response': self.response,
            'error': self.error
        })


class ClearDatabase(APIView):
    error = False
    response = ""

    def post(self, request):
        try:
            activity = request['activity']
            data = SensorData.objects.filter(activity=activity)
            data.delete()

        except Exception as e:
            self.error = True

        return Response({
            'response': self.response,
            'error': self.error
        })


def update_view(sender, instance, **kwargs):
    prediction = lstm(instance)

    return prediction
    # print("[" + str(instance.instant) + "]: " + prediction)


post_save.connect(update_view, sender=SensorData)
