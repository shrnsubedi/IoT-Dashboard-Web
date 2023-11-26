from django.contrib import admin

# Register your models here.
from sensor.models import Preferences, Room, Sensor, SensorReading


class SensorModelAdmin(admin.ModelAdmin):
    list_display = ("name", "room", "is_active", "is_alive")


admin.site.register(Sensor, SensorModelAdmin)
admin.site.register(SensorReading)
admin.site.register(Room)
admin.site.register(Preferences)
