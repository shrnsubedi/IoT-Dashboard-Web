from sensor.models import Sensor, SensorReading, Room
from django.utils import timezone
from datetime import timedelta


def get_latest_readings():
    sensors = Sensor.objects.all()
    rooms = Room.objects.all()

    all_rooms_data = {}

    for room in rooms:
        room_data = {}
        for sensor in sensors:
            latest_reading = (
                SensorReading.objects.filter(room=room, sensor=sensor)
                .order_by("-time")
                .first()
            )

            if latest_reading:
                room_data[sensor.name] = {
                    "value": latest_reading.value,
                    "timestamp": latest_reading.time.strftime("%Y-%m-%d %H:%M:%S"),
                }
        all_rooms_data[room.name] = room_data
    return all_rooms_data


def get_room_rankings(latest_readings):
    preferences = {"Temperature": 12, "Humidity": 54, "light": 2, "noise": 0}
    sensor_names = preferences.keys()

    room_rankings = []

    for room_name, room_data in latest_readings.items():
        score = sum(
            abs(room_data[sensor_name]["value"] - preferences[sensor_name])
            for sensor_name in sensor_names
            if sensor_name in room_data
        )
        room_rankings.append({"room": room_name, "score": score})

    sorted_rooms = sorted(room_rankings, key=lambda x: x["score"])
    return sorted_rooms
