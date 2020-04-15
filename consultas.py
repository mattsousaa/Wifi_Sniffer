#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
import string
import paho.mqtt.client as mqtt
from pymongo import MongoClient

broker = "localhost" # define o host do broker mqtt'
port = 1883 # define a porta do broker
keppAlive = 60 # define o keepAlive da conexao
topic = 'SPI/#' # define o topico que este script assinara

clienteMongo = MongoClient('localhost', 27017)
banco = clienteMongo.content
album = banco.test_collection

try:
    while(1):
        postT = ""
        op = input("\n\n\n1 - Consultar a última ocorrência de um MAC \n2 - Consultar todos os MACs\n3 - Consultar todas as ocorrências de um MAC\n")
        if (op == 1):
            macSearch = input("Digite o MAC:\n")
            macSearch = macSearch.lower()
            for post in album.find({"MAC": macSearch}).sort("TIME"):
                postT = post
            print(postT)
        elif (op == 2):
            for post in album.find():
                print(post)

        elif (op == 3):
            macSearch = input("Digite o MAC:\n")
            macSearch = macSearch.lower()
            for post in album.find({"MAC": macSearch}):
                print(post)

        elif (op == 123321):
            album.delete_many({})
            print("Finish")

        else:
            print("ERROR")

    
except KeyboardInterrupt:
    print("\nScript finalizado.")    
    sys.exit(0)
