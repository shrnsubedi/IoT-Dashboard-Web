from functools import wraps

from django.http import JsonResponse

from sensor.models import APIKey, Preferences, Room, Sensor, SensorReading


def get_latest_readings():
    rooms = Room.objects.all()

    all_rooms_data = {}

    for room in rooms:
        room_data = {}
        sensors = Sensor.objects.filter(room=room, is_active=True)

        for sensor in sensors:
            latest_reading = (
                SensorReading.objects.filter(sensor=sensor).order_by("-time").first()
            )

            if latest_reading:
                room_data[sensor.name] = {
                    "value": latest_reading.value,
                    "timestamp": latest_reading.time.strftime("%Y-%m-%d %H:%M:%S"),
                }
        all_rooms_data[room.name] = room_data

    return all_rooms_data


def get_room_rankings(latest_readings, user):
    preferences = {
        "Light": [500, 3],
        "Sound": [40, 3],
        "Humidity": [54, 3],
        "Temperature": [12, 3],
    }

    if user.is_authenticated:
        preference_obj = Preferences.objects.filter(user=user).first()
        if preference_obj:
            preferences = preference_obj.value
    sensor_names = preferences.keys()

    room_rankings = []

    for room_name, room_data in latest_readings.items():
        score = sum(
            abs(1 - room_data[sensor_name]["value"] / preferences[sensor_name][0])
            * preferences[sensor_name][1]
            for sensor_name in sensor_names
            if sensor_name in room_data
        )
        room_rankings.append({"room": room_name, "score": score})

    sorted_rooms = sorted(room_rankings, key=lambda x: x["score"])
    return sorted_rooms


# Decorator to check api-key
def token_required(f):
    @wraps(f)
    def decorated_function(request):
        token = request.headers.get("Token")
        api_key = APIKey.objects.first()

        if not token or token != api_key.key:
            return JsonResponse({"message": "Unauthorized"}, status=401)

        return f(request)

    return decorated_function
