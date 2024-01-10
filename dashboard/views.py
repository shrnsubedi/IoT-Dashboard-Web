import json
from datetime import datetime
from typing import Any

from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic

from sensor.models import Preferences, Room
from sensor.utils import get_latest_readings, get_room_rankings

# Create your views here.


class DashboardDataView(generic.TemplateView):
    template_name = "dashboard/landing.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["room_names"] = [room.name for room in Room.objects.all()]
        context["today_date"] = datetime.now().date

        return context


class DashboardDataAPI(generic.View):
    def get(self, request, *args, **kwargs):
        sensor_data = get_latest_readings()
        rankings = get_room_rankings(sensor_data, request.user)
        if sensor_data:
            return JsonResponse({"sensorData": sensor_data, "rankingData": rankings})
        else:
            return JsonResponse(
                {"error": "No data available for the specified room"}, status=400
            )


class PreferencesView(generic.View):
    template_name = "dashboard/preferences.html"

    def get(self, request, *args, **kwargs):
        preferences, created = Preferences.objects.get_or_create(user=request.user)
        initial_data = preferences.value if preferences.value else None

        return render(request, self.template_name, {"initial_data": initial_data})

    def post(self, request, *args, **kwargs):
        if request.content_type == "application/json":
            preferences_data = json.loads(request.body)
            preferences, created = Preferences.objects.get_or_create(user=request.user)
            preferences.value = preferences_data
            preferences.save()
            return JsonResponse({"status": "Preferences saved successfully"})
        else:
            return JsonResponse({"error": "Invalid content type"}, status=400)
