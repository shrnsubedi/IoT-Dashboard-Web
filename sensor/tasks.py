from datetime import timedelta

from background_task import background
from django.utils import timezone

from sensor.models import Sensor


@background()
def monitor_sensor_status():
    print("running")
    sensors = Sensor.objects.prefetch_related("sensor_reading").all()

    current_time = timezone.now()

    for sensor in sensors:
        last_reading = sensor.sensor_reading.latest("time")
        time_difference = current_time - last_reading.time

        # Update is_alive based on time difference
        sensor.is_alive = time_difference <= timedelta(minutes=5)

    # Batch update all sensors
    Sensor.objects.bulk_update(sensors, ["is_alive"])


monitor_sensor_status(schedule=10, repeat=300)
