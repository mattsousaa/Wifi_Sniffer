#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
import pymongo
import paho.mqtt.client as mqtt
from pymongo import MongoClient

broker = "localhost" # define o host do broker mqtt'
port = 1883 # define a porta do broker
keppAlive = 60 # define o keepAlive da conexao
topic = 'SPI/#' # define o topico que este script assinara

clienteMongo = MongoClient('localhost', 27017)
banco = clienteMongo.content
album = banco.test_collection

spi_client = pymongo.MongoClient(
    'mongodb+srv://admin:admin@mylove-jqsvg.gcp.mongodb.net/test?retryWrites=true'
)
cloud_database = spi_client.spi_proj
cloud_collection = cloud_database.node_track

contadorMsg = 1

# funcao on_connect sera atribuida e chamada quando a conexao for iniciada
# ela printara na tela caso tudo ocorra certo durante a tentativa de conexao
# tambem ira assinar o topico que foi declarado acima

def on_connect(client, userdata, flags, rc):
    print("[STATUS] Conectado ao Broker.")

    client.subscribe(topic)

# possui o mesmo cenario que o on_connect, porem, ela sera atrelada ao loop
# do script, pois toda vez que receber uma nova mensagem do topico assinado, ela sera invocada
def on_message(client, userdata, msg):
    print("Mensagem recebida")
    message = msg.payload.decode("utf-8")  # converte a mensagem recebida
    global contadorMsg
    if(contadorMsg == 99):
        sys.exit(0)  
    dicMessage = json.loads(message)
    listMAC = dicMessage['MAC']
    listRSSI = dicMessage['RSSI']
    time = dicMessage['TIME']
    node = dicMessage['NODE'] 
    for cont in range(0, len(listRSSI)):
        dist = 10 ** ((53 - ((-1)*listRSSI[cont]))/-20)
        messageSave = {"NODE": node, "MAC": listMAC[cont], "RSSI": listRSSI[cont], "TIME": time, "DIST": dist }
        album.insert_one(messageSave).inserted_id
        cloud_collection.insert_one(messageSave).inserted_id
    print(str(contadorMsg) + " Inserido")
    contadorMsg += 1  
try:
    print("[STATUS] Inicializando MQTT...")
    client = mqtt.Client() # instancia a conexao
    client.on_connect = on_connect # define o callback do evento on_connect
    client.on_message = on_message # define o callback do evento on_message
    client.connect(broker, port, keppAlive) # inicia a conexao
    client.loop_forever() # a conexao mqtt entrara em loop ou seja, ficara escutando e processando todas mensagens recebidas
    
except KeyboardInterrupt:
    print("\nScript finalizado.")    
    sys.exit(0)
