import os


MQTT_HOST = 'test.mosquitto.org'
MQTT_PORT = 1883
MQTT_KEEPALIVE = os.environ.get('KEEPALIVE', '60')
MEAN_PERIOD = os.environ.get('MEAN_PERIOD', '10')
SENSOR_TYPE = os.environ.get('SENSOR_TYPE', 'temperature')
CALCULATION_TIME_INTERVAL = os.environ.get('CALCULATION_TIME_INTERVAL', '5')
LOGGING_CONFIG = os.environ.get('LOGGING_CONFIG', '10')
