from typing import Any
from django.views import generic

from django.views import View
from django.http import JsonResponse

from sensor.models import Sensor, Room
from sensor.utils import get_latest_readings, get_room_rankings

# Create your views here.


class DashboardDataView(generic.TemplateView):
    template_name = "dashboard/landing.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["room_names"] = [room.name for room in Room.objects.all()]
        context["sensor_names"] = [sensor.name for sensor in Sensor.objects.all()]
        return context


class DashboardDataAPI(View):
    def get(self, request, *args, **kwargs):
        sensor_data = get_latest_readings()
        rankings = get_room_rankings(sensor_data)
        if sensor_data and rankings:
            return JsonResponse({"sensorData": sensor_data, "rankingData": rankings})
        else:
            return JsonResponse(
                {"error": "No data available for the specified room"}, status=400
            )
