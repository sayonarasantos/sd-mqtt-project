import time
import logging

import paho.mqtt.client as mqtt
import numpy as np

from config import MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE, MEASURED_VALUES_LIST_SIZE, MEASURED_VALUE_MIN, MEASURED_VALUE_MAX, MESSAGE_TIME_INTERVAL, SENSOR_TYPE, LOGGING_CONFIG


# Essa função trata o retorno de chamada (callback) quando há uma solicitação de conexão com o servidor MQTT.
# Quando o rc (return code) é zero, a conexão ocorreu com sucesso. Caso contrário, a conexão foi recusada.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info(f"CONNECTION -- * {SENSOR_TYPE} sensor connected to MQTT Broker.*")
    else:
        logging.error(f"CONNECTION -- * {SENSOR_TYPE} sensor failed to connect, returned code: {rc}.*")


# Essa função trata o callback quando há uma solicitação de disconexão com o servidor MQTT.
# Quando o rc (return code) é zero, a disconexão ocorreu com sucesso. Caso contrário, houve um erro nessa solicitação.
def on_disconnect(client, userdata, rc):
    if rc == 0:
        logging.info(f"CONNECTION -- * {SENSOR_TYPE} sensor disconnected to MQTT Broker.*")
    else:
        logging.error(f"CONNECTION -- * {SENSOR_TYPE} sensor fails to disconnect, returned code: {rc}.*")


# Essa função gera um array de valores aleatórios que simularam as temperaturas medidas pelo sensor.
def generate_measured_values(min_value, max_value, list_size):
    values = np.random.uniform(min_value, max_value, list_size)
    rounded_values = [round(value, 2) for value in values]

    return rounded_values


# Essa função publica cada item de um array de valores (gerado pela função anterior) no subtópico do sensor.
# Nessa aplicação, o tópico é 'sensors/temperature'.
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

    # Cria uma instância do cliente MQTT.
    mqtt_client = mqtt.Client()

    # Atribui a função on_connect (criada neste script) ao callback do cliente MQTT.
    mqtt_client.on_connect = on_connect
    # Atribui a função on_disconnect (criada neste script) ao callback do cliente MQTT.
    mqtt_client.on_disconnect = on_disconnect

    # Solicita a conexão com o servidor MQTT.
    mqtt_client.connect(MQTT_HOST, port=int(MQTT_PORT), keepalive=int(MQTT_KEEPALIVE))
    
    # Cria um array de valores de temperatura.
    measured_values = generate_measured_values(float(MEASURED_VALUE_MIN), float(MEASURED_VALUE_MAX),
                                               int(MEASURED_VALUES_LIST_SIZE))
    
    # Publica cada um dos valores do array criado no tópico do servidor MQTT.
    publish_messages(mqtt_client, SENSOR_TYPE, measured_values, int(MESSAGE_TIME_INTERVAL))
    
    # Encerra a conexão.
    mqtt_client.disconnect()
