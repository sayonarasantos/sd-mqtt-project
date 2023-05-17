import os


MQTT_HOST = os.environ.get('MQTT_HOST', 'test.mosquitto.org')
MQTT_PORT = os.environ.get('MQTT_PORT', '1883')
MQTT_KEEPALIVE = os.environ.get('MQTT_KEEPALIVE', '240')
MEASURED_VALUES_LIST_SIZE = os.environ.get('MEASURED_VALUES_LIST_SIZE', '20')
MEASURED_VALUE_MIN = os.environ.get('MEASURED_VALUE_MIN', '0')
MEASURED_VALUE_MAX = os.environ.get('MEASURED_VALUE_MAX', '300')
MESSAGE_TIME_INTERVAL = os.environ.get('MESSAGE_TIME_INTERVAL', '60')
SENSOR_TYPE = os.environ.get('SENSOR_TYPE', 'temperature')
LOGGING_CONFIG = os.environ.get('LOGGING_CONFIG', '10')
