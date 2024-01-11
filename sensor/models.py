from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Sensor(models.Model):
    name = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="sensors")
    is_active = models.BooleanField(default=True)
    is_alive = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.room}-{self.name}"


class SensorReading(models.Model):
    time = models.DateTimeField(default=datetime.now)
    sensor = models.ForeignKey(
        Sensor, on_delete=models.CASCADE, related_name="sensor_reading"
    )
    value = models.FloatField()

    def __str__(self) -> str:
        return f"{self.sensor}-{self.time}"

    def validate_unique(self, exclude=None):
        qs = SensorReading.objects.filter(sensor=self.sensor, time=self.time)
        if qs.exists():
            raise ValidationError(
                "Sensor Reading with this sensor and time already exists."
            )
        super().validate_unique(exclude)

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(SensorReading, self).save(*args, **kwargs)


class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    value = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user}-preferences"


class APIKey(models.Model):
    organization = models.CharField(max_length=50)
    key = models.CharField(max_length=50)
