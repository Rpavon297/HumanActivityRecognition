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
        'prediction': 'walking',
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

            self.response = LSTM(data)
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
            data = SensorData(accelx=request.data['accelx'],
                              accely=request.data['accely'],
                              accelz=request.data['accelz'],
                              gyrox=request.data['gyrox'],
                              gyroy=request.data['gyroy'],
                              gyroz=request.data['gyroz'],
                              velx=request.data['velx'],
                              vely=request.data['vely'],
                              velz=request.data['velz'],
                              instant=request.data['instant'],
                              activity=request.data['activity'])
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

def update_view(sender, instance, **kwargs):
    data = instance

    prediction = "first loop."
    if data.accelx == "2":
        prediction = "second loop."
    if data.accelx == "3":
        prediction = "third loop."

    print("[" + str(data.instant) + "]: " + prediction)


def LSTM(data):
        prediction = "first loop."
        if data.accelx == "2":
            prediction = "second loop."
        if data.accelx == "3":
            prediction = "third loop."

        return prediction


# post_save.connect(update_view, sender=SensorData)
