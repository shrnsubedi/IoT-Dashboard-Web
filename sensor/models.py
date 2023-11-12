from datetime import datetime
from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Sensor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class SensorReading(models.Model):
    class Meta:
        unique_together = (('sensor', 'time', 'room'),)

    time = models.DateTimeField(primary_key=True, default=datetime.now)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)