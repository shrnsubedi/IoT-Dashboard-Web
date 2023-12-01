import json

import paho.mqtt.client as mqtt
from django.conf import settings

from sensor.models import Room, Sensor, SensorReading


def parse_message(msg):
    time = msg["Time"]
    temperature = msg["Temperature"]
    humidity = msg["Humidity"]
    light = msg["Light Level"]
    sound = msg["Sound Level"]
    room = msg["Room"]

    return (
        time,
        room,
        {
            "Humidity": humidity,
            "Light": light,
            "Sound": sound,
            "Temperature": temperature,
        },
    )


def create_reading(msg):
    time, room, sensor_values = parse_message(msg)
    room = Room.objects.filter(name=room).first()
    for key, value in sensor_values.items():
        sensor = Sensor.objects.filter(name=key, room=room).first()
        SensorReading.objects.create(time=time, value=value, sensor=sensor)
    return 1


def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        mqtt_client.subscribe("AIPL/hr33ke2L/sensor/AIP_S108")
    else:
        print("Bad connection. Code:", rc)


def on_message(mqtt_client, userdata, msg):
    print(f"Received message on topic: {msg.topic} with payload: {msg.payload}")
    create_reading(json.loads(msg.payload))
    print("created reading")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE,
)
client.loop_start()
