from django.db import models


class SensorData(models.Model):
    accelx = models.CharField(max_length=30, null=False)
    accely = models.CharField(max_length=30, null=False)
    accelz = models.CharField(max_length=30, null=False)

    gyrox = models.CharField(max_length=30, null=False)
    gyroy = models.CharField(max_length=30, null=False)
    gyroz = models.CharField(max_length=30, null=False)

    orientx = models.CharField(max_length=30, null=False)
    orienty = models.CharField(max_length=30, null=False)
    orientz = models.CharField(max_length=30, null=False)

    sequence = models.CharField(max_length=100, null=False)

    activity = models.CharField(max_length=100, null=True)

    instant = models.DateTimeField()


class CurrentActivity(models.Model):
    device_key = models.CharField(max_length=100, null=False)
    activity = models.CharField(max_length=100, null=False)
