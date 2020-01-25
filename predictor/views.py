from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db.models.signals import post_save
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from predictor.models import SensorData
from predictor.serializers import SensorDataSerializer


def index(request):
    context = {
        'prediction': 'prediction here',
        'data': 'data here'
    }
    return render(request, 'index.html', context=context)


class MakePrediction(APIView):
    error = False
    response = ""

    def post(self, request):
        try:
            data = SensorData(accelx=request.data['accelx'],
                              accely=request.data['accely'],
                              accelz=request.data['accelz'],
                              gyrox=request.data['gyrox'],
                              gyroy=request.data['gyroy'],
                              gyroz=request.data['gyroz'],
                              velx=request.data['velx'],
                              vely=request.data['vely'],
                              velz=request.data['velz'],
                              instant=request.data['instant'])

            self.response = lstm(data)
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
                                  velx=sensorCapture['velx'],
                                  vely=sensorCapture['vely'],
                                  velz=sensorCapture['velz'],
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

    def post(self, request):
        try:
            clas = request.data['activity']

            data = SensorData.objects.filter(activity=clas)
            self.response = SensorDataSerializer(data, many=True).data

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
            data = SensorData.objects.all()
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


def lstm(data):
        prediction = "first loop."
        if data.accelx == "2":
            prediction = "second loop."
        if data.accelx == "3":
            prediction = "third loop."

        return prediction


post_save.connect(update_view, sender=SensorData)
