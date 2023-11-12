from typing import Any
from django.views import generic

from sensor.models import Sensor, SensorReading

# Create your views here.
class LandingPage(generic.TemplateView):
    template_name="dashboard/landing.html"

    def build_dashboard_data(self):
        sensor_data = SensorReading.objects.all().order_by("sensor")
        sensor_data.group_by = [""]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return