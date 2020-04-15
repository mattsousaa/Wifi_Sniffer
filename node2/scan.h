#include <NTPClient.h>
#include "ESP8266HTTPClient.h"
#include <WiFiUdp.h>
#include <ArduinoJson.h>
#include <set>
#include <time.h>
#include <string>
#include "./functions.h"
#include "./mqtt.h"
#include <ESP8266WiFi.h>


#define PURGETIME 600000
#define MAXDEVICES 60
#define JBUFFER 15+ (MAXDEVICES * 40)
#define disable 0
#define enable  1
#define TopicMQTT "SPI"
#define SENDTIME 30000
#define MINRSSI -99

char jsonString[JBUFFER];
const char* mqttUser = "admin";
const char* mqttPassword = "admin";
const char* ssid = "SPEEDFIBRA-9CEC";
const char* password =  "garotaipanema032977";

void connectToWiFi() {
  
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

/* The callback function will handle with the incoming messages for 
the topics subscribed. This function is used for startup tests.*/

void callback(char* topic, byte* payload, unsigned int length) {
 
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
 
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
 
  Serial.println();
  Serial.println("---------------------------");
 
}

void getHTTPDate(){
  const char * headerKeys[] = {"date", "server"} ;
  const size_t numberOfHeaders = 2;

  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status

    HTTPClient http;

    http.begin("http://www.google.com.br");

    http.collectHeaders(headerKeys, numberOfHeaders);

    int httpCode = http.GET();

    if (httpCode > 0) {
      for (int i = 0; i < http.headers(); i++) {
        Serial.println(http.header(i));
      }

      String headerDate = http.header("date");
      Serial.println(headerDate);

      String headerServer = http.header("server");
      Serial.println(headerServer);

      Serial.println("--------------------");

    } else {
      Serial.println("An error occurred sending the request");
    }

   }
}

void connectToMQTT(){
  
  // Setup MQTT  
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected()) {
    
    Serial.println("Connecting to MQTT...");

    if (client.connect("ESP8266Client", mqttUser, mqttPassword)){
      Serial.println("connected");
    } else {
      Serial.print("failed with state ");
      Serial.println(client.state());
    }

    client.publish("SPI", "Hello from ESP8266");
    //client.subscribe("esp/test");

    //yield();
  }
}

void sendDevices(String jsonRecebido) {
  String deviceMac;
  
  strncpy(jsonString, jsonRecebido.c_str(), jsonRecebido.length());
  //Serial.println(jsonString);
  
  if (client.publish(TopicMQTT, jsonString) == 1) Serial.println("Successfully published");
  else {
    Serial.println();
    Serial.println("!!!!! Not published. Please add #define MQTT_MAX_PACKET_SIZE 2048 at the beginning of PubSubClient.h file");
    Serial.println();
  }
}
