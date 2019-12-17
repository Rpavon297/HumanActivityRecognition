from django.db import models


class SensorData(models.Model):
    x = models.DecimalField(max_digits=30, decimal_places=10)
    y = models.DecimalField(max_digits=30, decimal_places=10)
    z = models.DecimalField(max_digits=30, decimal_places=10)
    instant = models.DateField()
