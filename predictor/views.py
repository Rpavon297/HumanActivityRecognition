import random
import string

import numpy as np
import SimplifiedHAR as harnet
import matlab

from matplotlib import pyplot as plt
from django.db.models import Q

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db.models.signals import post_save
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from datetime import datetime

from predictor.models import SensorData, CurrentActivity
from predictor.serializers import SensorDataSerializer

session = {}


def start_up():
    print('Initializing neural network...')
    session['handle'] = harnet.initialize()
    session['prediction'] = {
        "activity": "No data",
        "chance": "0"
    }


def index(request):
    sensordata = SensorData.objects.all()
    data = SensorDataSerializer(sensordata, many=True).data
    classes = [];

    for point in data:
        if point['activity'] not in classes:
            classes.append(point['activity']);

    context = {
        'current': session['prediction']['activity'],
        'chance': session['prediction']['chance'],
        'time': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
    }
    return render(request, 'index.html', context=context)


def current(request):
    if request.is_ajax():
        return JsonResponse({
            'current': session['prediction']['activity'],
            'chance': session['prediction']['chance'],
            'time': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        })


def invalids(request):
    data = SensorData.objects.all()
    invalid_data = SensorData.objects.filter(
        Q(accelx='NaN') | Q(accely='NaN') | Q(accelz='NaN') | Q(gyrox='NaN') | Q(gyroy='NaN') | Q(gyroz='NaN') |
        Q(orientx='NaN') | Q(orienty='NaN') | Q(orientz='NaN'))
    all_rows = SensorDataSerializer(data, many=True).data
    invalid_rows = SensorDataSerializer(invalid_data, many=True).data

    bad = len(invalid_rows)
    good = len(all_rows) - bad

    percent = (bad / good) * 100

    print(percent)
    print("deleting...")

    invalid_data.delete()

    return JsonResponse({
        'valids': good,
        'invalids': bad
    })


def lstm(data):
    data_list = data.tolist()

    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            data_list[i][j] = float(data_list[i][j])

    prediction = session['handle'].predict(matlab.double(data_list))
    # activity = prediction['activity']
    # chance = prediction['chance']
    # print(activity)
    # print(chance)
    return prediction


def plot(data):
    plt.title("Datos en movimiento en el eje X para alfa 0.2")
    plt.xlabel("Capturas")
    plt.ylabel("Orientación")

    for row in data:
        x = row['points']
        label = row['label']

        y = np.arange(1, len(x) + 1)
        plt.plot(y, x, label=label)

    plt.legend()
    plt.show()


class PlotData(APIView):
    error = False
    response = ""
    handle = None

    def post(self, request):
        try:
            data_accel = [
                {
                    'points': request.data['captures']['raw_accel'],
                    'label': "Ac. lineal sin filtrar"
                },
                {
                    'points': request.data['captures']['filtered_accel'],
                    'label': "Ac. lineal tras filtrar"
                }]

            data_rotat = [
                {
                    'points': request.data['captures']['raw_rotat'],
                    'label': "Ac. angular sin filtrar"
                },
                {
                    'points': request.data['captures']['filtered_rotat'],
                    'label': "Ac. tras filtrar"
                }]

            data_orient = [
                {
                    'points': request.data['captures']['raw_orient'],
                    'label': "Orientación sin filtrar"
                },
                {
                    'points': request.data['captures']['filtered_orient'],
                    'label': "Orientación tras filtrar"
                }]

            plot(data_accel)
            plot(data_rotat)
            plot(data_orient)
        except Exception as e:
            self.error = True
        return Response({
            'response': self.response,
            'error': self.error
        })


class MakePrediction(APIView):
    error = False
    response = ""
    handle = None

    def post(self, request):
        try:
            package = request.data['captures']
            x = []

            for sensorCapture in package:
                row = []
                for item in ['accelx', 'accely', 'accelz', 'gyrox', 'gyroy', 'gyroz', 'orientx', 'orienty', 'orientz']:
                    row.append(sensorCapture[item])
                x.append(row)
            x = np.transpose(x)

            session['prediction'] = lstm(x)
            session['prediction']['chance'] = session['prediction']['chance'] * 100

            self.response = session['prediction']['activity']

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
            data = SensorData.objects.filter(activity="Sitting")
            data.delete()

        except Exception as e:
            self.error = True

        return Response({
            'response': self.response,
            'error': self.error
        })
