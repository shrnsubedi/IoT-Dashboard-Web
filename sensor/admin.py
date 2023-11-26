from django.contrib import admin

# Register your models here.
from sensor.models import Preferences, Room, Sensor, SensorReading

admin.site.register(Sensor)
admin.site.register(SensorReading)
admin.site.register(Room)
admin.site.register(Preferences)
