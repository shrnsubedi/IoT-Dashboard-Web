from django.utils import timezone
from datetime import timedelta

from typing import Any
from django.views import generic
from django.http import JsonResponse
from django.views import View

from sensor.models import Sensor, SensorReading, Room

# Create your views here.

class LandingPageView(generic.TemplateView):
    template_name="dashboard/landing.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["room_names"] = [room.name for room in Room.objects.all()]
        return context

class LatestSensorDataView(View):
    def get(self, request, *args, **kwargs):
        room_name = request.GET.get('room_name')
        room = Room.objects.get(name=room_name)
        
        sensors = Sensor.objects.all()

        sensor_data = {}

        for sensor in sensors:
            latest_reading = SensorReading.objects.filter(
                room=room, sensor=sensor
            ).order_by('-time').first()

            if latest_reading:
                sensor_data[sensor.name] = {
                    'value': latest_reading.value,
                    'timestamp': latest_reading.time.strftime('%Y-%m-%d %H:%M:%S'),
                }
        print(sensor_data)
        if sensor_data:
            return JsonResponse(sensor_data)
        else:
            return JsonResponse({'error': 'No data available for the specified room'}, status=400)