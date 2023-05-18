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


# Essa função trata o retorno de chamada (callback) quando há uma solicitação de conexão com o servidor MQTT.
# Quando o rc (return code) é zero, a conexão ocorreu com sucesso. Caso contrário, a conexão foi recusada.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info(f"CONNECTION -- * Alarm connected to MQTT Broker.*")
    else:
        logging.error(f"CONNECTION -- * Alarm failed to connect, returned code: {rc}.*")


# Essa função trata o callback quando o cliente se inscreve em um tópico do servidor MQTT.
def on_subscribe(client, userdata, mid, granted_qos):
    global topic

    logging.info(f"SUBSCRIPTION -- * Alarm subscribed to topic: {topic}.*")


# Essa função trata o callback quando o cliente recebe uma mensagem no tópico do servidor MQTT.
# Para as mensagens de temperatura alta (high_temperature) e mudança brusca de temperatura (sudden_temperature_increase),
# é solicitada a criação de alarmes.
def on_message(client, userdata, message):
    payload = message.payload.decode()

    logging.debug(f"SUBSCRIPTION -- * Message received in topic {message.topic}, payload: {payload}.*")

    if(payload == "high_temperature"):
        create_alarm("The temperature of the environment is high.")
    
    if(payload == "sudden_temperature_increase"):
        create_alarm("The temperature of the environment has changed suddenly.")


# Essa função cria os alarmes adicionando a mensagem e o horário do alarme na lista messages.
# A lista será exibida na página web, que mostra apenas os cinco últimos alarmes.
def create_alarm(message):
    global messages

    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    messages.append((current_time, message))

    if len(messages) > 5:
        messages.pop(0)


# Essa função inicia o cliente MQTT
def start_mqtt_client():
    # Cria uma instância do cliente MQTT.
    mqtt_client = mqtt.Client()

    # Atribui a função on_connect (criada neste script) ao callback do cliente MQTT.
    mqtt_client.on_connect = on_connect
    # Atribui a função on_subscribe (criada neste script) ao callback do cliente MQTT.
    mqtt_client.on_subscribe = on_subscribe
    # Atribui a função on_message (criada neste script) ao callback do cliente MQTT.
    mqtt_client.on_message = on_message

    # Solicita a conexão com o servidor MQTT.
    mqtt_client.connect(MQTT_HOST, port=int(MQTT_PORT), keepalive=int(MQTT_KEEPALIVE))
    # Inscreve-se no tópico da calculadora para receber as mensagens das médias das temperaturas.
    mqtt_client.subscribe(topic)

    # Inicia um laço infinito de eventos.
    mqtt_client.loop_forever()


# Quando acessamos a rota raíz, iniciamos uma thread para iniciar o cliente e deixar laço de eventos em execução.
# Depois o usuário é direcionar para a página de alarmes.
@app.route('/')
def index():
    mqtt_thread = threading.Thread(target=start_mqtt_client)
    mqtt_thread.start()
    
    return redirect(url_for('alarms'))


# Nessa rota, a lista de mensagens é exibida.
@app.route('/alarms')
def alarms():
    global messages

    return render_template('index.html', messages=messages)


if __name__ == '__main__':
    logging.basicConfig(level=int(LOGGING_CONFIG))

    app.run(host='0.0.0.0', port=8080)
