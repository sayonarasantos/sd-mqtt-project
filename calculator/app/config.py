import os


MQTT_HOST = os.environ.get('MQTT_HOST', 'test.mosquitto.org')
MQTT_PORT = os.environ.get('MQTT_PORT', '1883')
MQTT_KEEPALIVE = os.environ.get('MQTT_KEEPALIVE', '240')
MEAN_PERIOD = os.environ.get('MEAN_PERIOD', '120')
SENSOR_TYPE = os.environ.get('SENSOR_TYPE', 'temperature')
LOGGING_CONFIG = os.environ.get('LOGGING_CONFIG', '10')
