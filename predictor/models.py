from django.db import models


class SensorData(models.Model):
    accelx = models.DecimalField(max_digits=30, decimal_places=10)
    accely = models.DecimalField(max_digits=30, decimal_places=10)
    accelz = models.DecimalField(max_digits=30, decimal_places=10)

    gyrox = models.DecimalField(max_digits=30, decimal_places=10)
    gyroy = models.DecimalField(max_digits=30, decimal_places=10)
    gyroz = models.DecimalField(max_digits=30, decimal_places=10)

    velx = models.DecimalField(max_digits=30, decimal_places=10)
    vely = models.DecimalField(max_digits=30, decimal_places=10)
    velz = models.DecimalField(max_digits=30, decimal_places=10)

    activity = models.CharField(max_length=100, null=True)

    instant = models.DateTimeField()
