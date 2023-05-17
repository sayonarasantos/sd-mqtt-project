import threading
import logging
import time
import os

from flask import Flask, render_template, redirect, url_for
import paho.mqtt.client as mqtt

from config import MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE, LOGGING_CONFIG

app = Flask(__name__, template_folder=os.path.abspath('templates'))
topic = 'calculator'
messages = list()


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
        create_alarm("The temperature of the environment is high.")
    
    if(payload == "sudden_temperature_increase"):
        create_alarm("The temperature of the environment has changed suddenly.")


def create_alarm(message):
    global messages

    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    messages.append((current_time, message))

    if len(messages) > 5:
        messages.pop(0)


def start_mqtt_client():
    mqtt_client = mqtt.Client()

    mqtt_client.on_connect = on_connect
    mqtt_client.on_subscribe = on_subscribe
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_HOST, port=int(MQTT_PORT), keepalive=int(MQTT_KEEPALIVE))
    mqtt_client.subscribe(topic)

    mqtt_client.loop_forever()


@app.route('/')
def index():
    mqtt_thread = threading.Thread(target=start_mqtt_client)
    mqtt_thread.start()
    
    return redirect(url_for('alarms'))


@app.route('/alarms')
def alarms():
    global messages

    return render_template('index.html', messages=messages)


if __name__ == '__main__':
    logging.basicConfig(level=int(LOGGING_CONFIG))

    app.run(host='0.0.0.0', port=8080)
