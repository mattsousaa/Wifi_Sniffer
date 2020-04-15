#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
import string
import pymongo
import paho.mqtt.client as mqtt
from pymongo import MongoClient

topic = 'SPI_SERVER/#' # define o topico que este script assinara

"""
Requisitos:
* Criar conta no MongoDB Atlas e um Cluster para uso pessoal
* Copiar endereço SRV para conexão remota

Instalar:
# python3 -m pip install pymongo --user
# python3 -m pip install dnspython --user

"""

# SRV de uso pessoal associada ao e-mail: mateuseng_ec@alu.ufc.br
spi_client = pymongo.MongoClient(
    'mongodb+srv://admin:admin@mylove-jqsvg.gcp.mongodb.net/test?retryWrites=true'
)
cloud_database = spi_client.spi_proj            # Procura no servidor o banco "spi_proj"
cloud_collection = cloud_database.node_track    # Faz consultas nesta label "node_track"

try:
    while(1):
        print("MongoDB version is %s" % spi_client.server_info()['version'])
        postT = ""
        op = input("\n1 - Consultar a última ocorrência de um MAC \n2 - Consultar todos os MACs\n3 - Consultar todas as ocorrências de um MAC\n")
        if (op == 1):
            macSearch = input("Digite o MAC:\n")
            macSearch = macSearch.lower()
            for post in cloud_collection.find({"MAC": macSearch}).sort("TIME"):
                postT = post
            print(postT)
        elif (op == 2):
            for post in cloud_collection.find():
                print(post)

        elif (op == 3):
            macSearch = input("Digite o MAC:\n")
            macSearch = macSearch.lower()
            for post in cloud_collection.find({"MAC": macSearch}):
                print(post)

        elif (op == 123321):
            cloud_collection.delete_many({})
            print("Finish")

        else:
            print("ERROR")

    
except KeyboardInterrupt:
    print("\nScript finalizado.")    
    sys.exit(0)
