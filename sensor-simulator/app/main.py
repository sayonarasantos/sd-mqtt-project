import time
import logging

import paho.mqtt.client as mqtt
import numpy as np

from config import MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE, MEASURED_VALUES_LIST_SIZE, MEASURED_VALUE_MIN, MEASURED_VALUE_MAX, MESSAGE_TIME_INTERVAL, SENSOR_TYPE, LOGGING_CONFIG


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info(f"CONNECTION -- * {SENSOR_TYPE} sensor connected to MQTT Broker.*")
    else:
        logging.error(f"CONNECTION -- * {SENSOR_TYPE} sensor failed to connect, returned code: {rc}.*")


def on_disconnect(client, userdata, rc):
    if rc == 0:
        logging.info(f"CONNECTION -- * {SENSOR_TYPE} sensor disconnected to MQTT Broker.*")
    else:
        logging.error(f"CONNECTION -- * {SENSOR_TYPE} sensor fails to disconnect, returned code: {rc}.*")


def generate_measured_values(min_value, max_value, list_size):
    values = np.random.uniform(min_value, max_value, list_size)
    rounded_values = [round(value, 2) for value in values]

    return rounded_values


def publish_messages(mqtt_client, sensor_type, values, message_time_interval):
    topic = f'sensors/{sensor_type}'

    for value in values:
        response = mqtt_client.publish(topic, value)

        if response.is_published:
            logging.debug(f"PUBLICATION -- * Value {value} published on topic {topic}.*")
        else:
            logging.error(f"PUBLICATION -- * Error publishing message, returned code: {response.rc}.*")
        
        time.sleep(message_time_interval)


if __name__ == "__main__":
    logging.basicConfig(level=int(LOGGING_CONFIG))

    mqtt_client = mqtt.Client()

    mqtt_client.on_connect = on_connect
    mqtt_client.on_disconnect = on_disconnect

    mqtt_client.connect(MQTT_HOST, port=MQTT_PORT, keepalive=int(MQTT_KEEPALIVE))
    
    measured_values = generate_measured_values(float(MEASURED_VALUE_MIN), float(MEASURED_VALUE_MAX), int(MEASURED_VALUES_LIST_SIZE))
    
    publish_messages(mqtt_client, SENSOR_TYPE, measured_values, int(MESSAGE_TIME_INTERVAL))
    
    mqtt_client.disconnect()
