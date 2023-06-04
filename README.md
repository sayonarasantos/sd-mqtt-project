# Projeto MQTT para a cadeira de Sistemas Distribuídos

Foram desenvolvidos três serviços que se comunicam por meio de um servidor MQTT:

- O simulador de sensores de temperatura
- A calculadora de média da temperatura
- A aplicação web de alarme relacionados a essa média.

Além disso, utiliza-se um servidor MQTT Mosquitto de forma self-hosted.

## Para executar as aplicações

### Pre-requisitos

- Docker e Docker Compose instalados

### Execução

- Iniciar as aplicações

    ```bash
    docker compose up -d
    ```

    O aplicação web de alarme fica disponível em [0.0.0.0:8080](0.0.0.0:8080).

- Parar as aplicações

    ```bash
    docker compose down
    ```
