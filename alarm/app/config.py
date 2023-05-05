import os


MQTT_HOST = os.environ.get('MQTT_HOST', 'test.mosquitto.org')
MQTT_PORT = os.environ.get('MQTT_PORT', '1883')
MQTT_KEEPALIVE = os.environ.get('KEEPALIVE', '60')
LOGGING_CONFIG = os.environ.get('LOGGING_CONFIG', '10')
