import time
import logging

import paho.mqtt.client as mqtt

from config import MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE, SENSOR_TYPE, MEAN_PERIOD, LOGGING_CONFIG


measured_values_times = list()
sensor_topic = f'sensors/{SENSOR_TYPE}'
last_mean_value = -100


# Essa função trata o retorno de chamada (callback) quando há uma solicitação de conexão com o servidor MQTT.
# Quando o rc (return code) é zero, a conexão ocorreu com sucesso. Caso contrário, a conexão foi recusada.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info(f"CONNECTION -- * Calculator connected to MQTT Broker.*")
    else:
        logging.error(f"CONNECTION -- * Calculator failed to connect, returned code: {rc}.*")


# Essa função trata o callback quando o cliente se inscreve em um tópico do servidor MQTT.
def on_subscribe(client, userdata, mid, granted_qos):
    global sensor_topic

    logging.info(f"SUBSCRIPTION -- * Calculator subscribed to topic: {sensor_topic}.*")


# Essa função trata o callback quando o cliente recebe uma mensagem no tópico do servidor MQTT.
# A mensagem recebida deve ser um valor de temperatura do sensor. Então a função tenta armazenar esse valor na lista
# measured_values_times junto do perído do recebimento da mensagem.
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


# Essa função calcula a média de temperatura com os valores presentes na lista measured_values_times.
# Cada elemento dessa lista é composto pela temperatura (measured_values_times[0]) e
# o perído do recebimento dessa temperatura (measured_values_times[1]).
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

                logging.debug(f"CALCULATION -- ** Measurement: time: {time.asctime(time.localtime(element[0]))} ;"
                              f" value: {element[1]}.**")

        if len(only_values) > 0:
            mean_values = round(sum(only_values) / len(only_values), 2)
            measured_values_times = updated_values_times

            logging.info(f"CALCULATION -- * Mean of measured values: {mean_values}.*")
    
    return mean_values


# Essa função verifica a média calculada e solicita a publicação de uma mensagem em dois casos:
# - Quando a média é maior que 200, mandando uma mensagem de temperatura alta;
# - Quando a diferença entre a média atual e a média anterior é maior que cinco,
#   mandando uma mensagem de mudança brusca de temperatura.
def check_mean(value, mqtt_client):
    global last_mean_value

    logging.debug(f"CALCULATION -- * Last mean: {last_mean_value}.*")

    if value > 200:
        publish_message(mqtt_client, "high_temperature")

    if last_mean_value != -100:
        delta = abs(last_mean_value - value)
        logging.debug(f"CALCULATION -- * Difference between means: {delta}.*")

        if (delta > 5):
            publish_message(mqtt_client, "sudden_temperature_increase")
    
    last_mean_value = value


# Essa função publica uma mensagem no tópico 'calculator'.
def publish_message(mqtt_client, message):
    topic = 'calculator'

    response = mqtt_client.publish(topic, message)

    if response.is_published:
        logging.debug(f"PUBLICATION -- * Message published on topic {topic}.*")
    else:
        logging.error(f"PUBLICATION -- * Error publishing message, returned code: {response.rc}.*")


if __name__ == "__main__":
    logging.basicConfig(level=int(LOGGING_CONFIG))

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
    # Inscreve-se no tópico dos sensores para receber as mensagens de temperatura enviadas por eles.
    mqtt_client.subscribe(sensor_topic)

    # Inicia o laço de eventos do cliente MQTT. Com isso, o cliente fica ativo para publicar e receber mensagens.
    mqtt_client.loop_start()

    # A cada MEAN_PERIOD (em segundos), esse laço verifica a média dos valores registrados pelos sensores e
    # realiza a publicação da mensagem dependendo da média obtida.
    while True:
        check_mean(calcule_mean(), mqtt_client)
        time.sleep(int(MEAN_PERIOD))