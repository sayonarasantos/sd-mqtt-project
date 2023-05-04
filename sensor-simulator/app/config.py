import os


MQTT_HOST = 'test.mosquitto.org'
MQTT_PORT = 1883
MQTT_KEEPALIVE = os.environ.get('KEEPALIVE', '60')
MEASURED_VALUES_LIST_SIZE = os.environ.get('VALUES_LIST_SIZE', '50')
MEASURED_VALUE_MIN = os.environ.get('MIN_VALUE', '150')
MEASURED_VALUE_MAX = os.environ.get('MAX_VALUE', '250')
MESSAGE_TIME_INTERVAL = os.environ.get('MESSAGE_TIME', '4')
SENSOR_TYPE = os.environ.get('SENSOR_TYPE', 'temperature')
LOGGING_CONFIG = os.environ.get('LOGGING_CONFIG', '10')
