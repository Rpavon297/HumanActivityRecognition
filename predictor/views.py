from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models.signals import post_save
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from predictor.models import SensorData


def index(request):
    context = {
        'prediction': 'walking',
    }
    return render(request, 'index.html', context=context)


@csrf_exempt
@require_POST
def update_data(request):
    data = SensorData(accelx=request.POST['accelx'],
                      accely=request.POST['accely'],
                      accelz=request.POST['accelz'],
                      gyrox=request.POST['gyrox'],
                      gyroy=request.POST['gyroy'],
                      gyroz=request.POST['gyroz'],
                      velx=request.POST['velx'],
                      vely=request.POST['vely'],
                      velz=request.POST['velz'],
                      instant=request.POST['instant'])
    data.save()
    return HttpResponse("")


def update_view(sender, instance, **kwargs):
    data = instance

    prediction = "first loop."
    if data.accelx == "2":
        prediction = "second loop."
    if data.accelx == "3":
        prediction = "third loop."

    print("[" + str(data.instant) + "]: " + prediction)


post_save.connect(update_view, sender=SensorData)
