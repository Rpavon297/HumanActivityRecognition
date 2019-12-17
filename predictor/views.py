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
    data = SensorData(x=request.POST['x'], y=request.POST['y'], z=request.POST['z'], instant=request.POST['instant'])
    data.save()
    return HttpResponse("a")


def update_view(sender, instance, **kwargs):
    print("ok")


post_save.connect(update_view, sender=SensorData)
