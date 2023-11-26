from sensor.models import Preferences, Room, Sensor, SensorReading


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
    if not user.is_authenticated:
        return None

    preferences_obj = Preferences.objects.filter(user=user).first()

    if not preferences_obj:
        return None

    preferences = preferences_obj.value
    sensor_names = preferences.keys()

    room_rankings = []

    for room_name, room_data in latest_readings.items():
        score = sum(
            abs(room_data[sensor_name]["value"] - preferences[sensor_name][0])
            * preferences[sensor_name][1]
            for sensor_name in sensor_names
            if sensor_name in room_data
        )
        room_rankings.append({"room": room_name, "score": score})

    sorted_rooms = sorted(room_rankings, key=lambda x: x["score"])
    return sorted_rooms
