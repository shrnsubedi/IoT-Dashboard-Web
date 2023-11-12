import paho.mqtt.client as mqtt
import json

from django.conf import settings
from sensor.models import Sensor, SensorReading

def parse_message(msg):
    time = msg["time"]
    value = msg["value"]
    sensor_name = msg["sensor"]
    return time, value, sensor_name

def create_reading(msg):
    time, value, sensor_name= parse_message(msg)
    sensor = Sensor.objects.filter(name = sensor_name).first()
    return SensorReading.objects.create(time=time, value=value, sensor=sensor)

def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe('AIPL/sensor/*')
    else:
        print('Bad connection. Code:', rc)

def on_message(mqtt_client, userdata, msg):
    print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
    reading = create_reading(json.loads(msg.payload))
    print(f'created reading')


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)
client.loop_start()