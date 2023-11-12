from django.contrib import admin

# Register your models here.
from sensor.models import Sensor, SensorReading, Room

admin.site.register(Sensor)
admin.site.register(SensorReading)
admin.site.register(Room)