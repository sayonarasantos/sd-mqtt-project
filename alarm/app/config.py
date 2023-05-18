# Nesse script é feita a configuração das variáveis utilizadas na aplicação
import os


MQTT_HOST = os.environ.get('MQTT_HOST', 'test.mosquitto.org')
MQTT_PORT = os.environ.get('MQTT_PORT', '1883')
MQTT_KEEPALIVE = os.environ.get('MQTT_KEEPALIVE', '240')
LOGGING_CONFIG = os.environ.get('LOGGING_CONFIG', '10')
