import time
import logging

import paho.mqtt.client as mqtt

from config import MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE, SENSOR_TYPE, MEAN_PERIOD, CALCULATION_TIME_INTERVAL, LOGGING_CONFIG


measured_values_times = list()
sensor_topic = f'sensors/{SENSOR_TYPE}'
last_mean_value = -100


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info(f"CONNECTION -- * Calculator connected to MQTT Broker.*")
    else:
        logging.error(f"CONNECTION -- * Calculator failed to connect, returned code: {rc}.*")


def on_subscribe(client, userdata, mid, granted_qos):
    global sensor_topic

    logging.info(f"SUBSCRIPTION -- * Calculator subscribed to topic: {sensor_topic}.*")


def on_message(client, userdata, message):
    global measured_values_times

    payload = message.payload.decode()

    logging.debug(f"SUBSCRIPTION -- * Message received in topic {message.topic}, payload: {payload}.*")
    
    try:
        measured_value = float(payload)
        measurement_time = time.time()
        measured_values_times.append((measurement_time, measured_value))
    except ValueError:
        logging.error("SUBSCRIPTION -- * {ValueError}.*")
        pass


def calcule_mean():
    global measured_values_times

    mean_values = 0
    current_time = time.time()
    updated_values_times = list()
    only_values = list()

    logging.debug(f"CALCULATION -- * Start loop, Current time: {time.asctime( time.localtime(current_time))}.*")

    if len(measured_values_times) > 0:
        for element in measured_values_times:
            if current_time - element[0] < float(MEAN_PERIOD):
                updated_values_times.append(element)
                only_values.append(element[1])

                logging.debug(f"CALCULATION -- ** Measurement: time: {time.asctime(time.localtime(element[0]))} ; value: {element[1]}.**")

        if len(only_values) > 0:
            mean_values = round(sum(only_values) / len(only_values), 2)
            measured_values_times = updated_values_times

            logging.info(f"CALCULATION -- * Mean of measured values: {mean_values}.*")
    
    return mean_values


def check_mean(value, mqtt_client):
    global last_mean_value

    if value > 200:
        publish_message(mqtt_client, "high_temperature")

    if last_mean_value != -100:
        delta = abs(last_mean_value - value)
        logging.debug(f"CALCULATION -- * Difference between means: {delta}.*")

        if (delta > 5):
            publish_message(mqtt_client, "sudden_temperature_increase")


def publish_message(mqtt_client, message):
    topic = 'calculator'

    response = mqtt_client.publish(topic, message)

    if response.is_published:
        logging.debug(f"PUBLICATION -- * Message published on topic {topic}.*")
    else:
        logging.error(f"PUBLICATION -- * Error publishing message, returned code: {response.rc}.*")


if __name__ == "__main__":
    logging.basicConfig(level=int(LOGGING_CONFIG))

    mqtt_client = mqtt.Client()

    mqtt_client.on_connect = on_connect
    mqtt_client.on_subscribe = on_subscribe
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_HOST, port=int(MQTT_PORT), keepalive=int(MQTT_KEEPALIVE))
    mqtt_client.subscribe(sensor_topic)

    mqtt_client.loop_start()

    while True:
        check_mean(calcule_mean(), mqtt_client)
        time.sleep(int(CALCULATION_TIME_INTERVAL))