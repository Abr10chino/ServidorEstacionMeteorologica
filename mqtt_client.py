import json
import paho.mqtt.client as mqtt
from crud import insertarLecturas

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "umes/clima"

def onConnect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Conectando al broker MQTT: {BROKER}")
        client.subscribe(TOPIC)
        print(f"Suscrito al tópico: {TOPIC}")
    else:
        print("Error al conectarse al broker MQTT:", rc)

def onMessage(client, userdata, msg):
    try:
        
        data = json.loads(msg.payload.decode("utf-8"))
        print(f"Mensaje recibido en {msg.topic}: {data}")
        if insertarLecturas(data):
            print("Datos insertados correctamente en la base de datos.")
        else:
            print("Error al insertar datos en la base de datos.")

    except Exception as e:
        print("Error al procesar el mensaje:", e)

def startMqtt():
    client = mqtt.Client()
    client.on_connect = onConnect
    client.on_message = onMessage
    client.connect(BROKER, PORT, keepalive=60)
    print(f"Iniciando MQTT Server ...")
    client.loop_forever()