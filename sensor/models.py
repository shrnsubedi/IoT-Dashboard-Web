from datetime import datetime
from django.db import models

# Create your models here.
class Sensor(models.Model):
    name = models.CharField(max_length=50)

class SensorReading(models.Model):
    class Meta:
        unique_together = (('sensor', 'time'),)

    time = models.DateTimeField(primary_key=True, default=datetime.now)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()