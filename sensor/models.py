from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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
        unique_together = (("sensor", "time", "room"),)

    time = models.DateTimeField(primary_key=True, default=datetime.now)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)


class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    value = models.JSONField()

    def __str__(self) -> str:
        return f"{self.user}-preferences"
