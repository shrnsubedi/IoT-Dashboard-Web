from datetime import timedelta

from django.contrib import admin
from django.utils import timezone

# Register your models here.
from sensor.models import Preferences, Room, Sensor, SensorReading


class SensorModelAdmin(admin.ModelAdmin):
    list_display = ("name", "room", "is_active", "is_alive")


class RoomAdmin(admin.ModelAdmin):
    change_form_template = "admin/sensor/room/change_form.html"

    def change_view(self, request, object_id, form_url="", extra_context=None):
        room_instance = self.get_object(request, object_id)
        chart_data = self.get_temperature_data(room_instance)

        extra_context = extra_context or {}
        extra_context["temperature_data"] = chart_data

        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context
        )

    def get_temperature_data(self, room):
        sensor_readings = SensorReading.objects.filter(
            sensor__room=room,
            sensor__name="Temperature",
            time__gte=timezone.now() - timedelta(hours=24),
        ).values("time", "value")
        sensor_readings = list(sensor_readings)
        temperature_data = [
            {"time": item["time"].isoformat(), "value": item["value"]}
            for item in sensor_readings
        ]

        return temperature_data


admin.site.register(Sensor, SensorModelAdmin)
admin.site.register(SensorReading)
admin.site.register(Room, RoomAdmin)
admin.site.register(Preferences)
