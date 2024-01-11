from datetime import timedelta

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from sensor.models import Room, SensorReading
from sensor.utils import token_required


@csrf_exempt
@token_required
def sensor_readings_api(request):
    if request.method == "GET":
        try:
            room = request.GET.get("room")
        except Exception:
            return JsonResponse({"message": "Room parameter is required"})

        room_obj = Room.objects.filter(name=room).first()
        if not room:
            return JsonResponse({"message": "Room name is not valid"})

        sensor_readings = SensorReading.objects.filter(
            sensor__room=room_obj.id,
            sensor__name="Temperature",
            time__gte=timezone.now() - timedelta(hours=24),
        ).values("time", "value")

        return JsonResponse(list(sensor_readings), safe=False)
