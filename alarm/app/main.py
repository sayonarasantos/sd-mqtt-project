import logging

import paho.mqtt.client as mqtt

from config import MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE, LOGGING_CONFIG


topic = 'calculator'


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info(f"CONNECTION -- * Alarm connected to MQTT Broker.*")
    else:
        logging.error(f"CONNECTION -- * Alarm failed to connect, returned code: {rc}.*")


def on_subscribe(client, userdata, mid, granted_qos):
    global topic

    logging.info(f"SUBSCRIPTION -- * Alarm subscribed to topic: {topic}.*")


def on_message(client, userdata, message):
    payload = message.payload.decode()

    logging.debug(f"SUBSCRIPTION -- * Message received in topic {message.topic}, payload: {payload}.*")

    if(payload == "high_temperature"):
        print("The temperature of the environment is high.")
    
    if(payload == "sudden_temperature_increase"):
        print("The temperature of the environment has changed suddenly.")


if __name__ == "__main__":
    logging.basicConfig(level=int(LOGGING_CONFIG))

    mqtt_client = mqtt.Client()

    mqtt_client.on_connect = on_connect
    mqtt_client.on_subscribe = on_subscribe
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_HOST, port=MQTT_PORT, keepalive=int(MQTT_KEEPALIVE))
    mqtt_client.subscribe(topic)

    mqtt_client.loop_forever()
