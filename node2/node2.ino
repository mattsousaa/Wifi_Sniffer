#include <string>
#include "scan.h"
#include <NTPClient.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

unsigned long tempoInicial = 0, tempoFinal = 0;
unsigned long int testeTime = 1000;
String jsonRecebido, jsonFinal;

WiFiUDP ntpUDP;

int16_t utc = -3; //UTC -3:00 Brazil
uint32_t currentMillis = 0;
uint32_t previousMillis = 0;

NTPClient timeClient(ntpUDP, "a.st1.ntp.br", utc * 3600, 60000);

void setup() {
  Serial.begin(115200);
  Serial.println("Iniciando...");
  connectToWiFi();
  timeClient.begin();
  timeClient.update();
  delay(500);
  Serial.println("Hora:" + timeClient.getFormattedTime());
  connectToMQTT();
}

void callback(char* topic, byte* payload, unsigned int length);

void loop() {

    if(Serial.available() > 0){
    tempoInicial = millis();
    jsonRecebido = Serial.readString();
    jsonRecebido.remove(jsonRecebido.lastIndexOf("}"));
    jsonFinal = jsonRecebido + ",\"TIME\":[" + "\"" + timeClient.getFormattedTime() + "\"]}"; 
    Serial.println(jsonFinal);
    client.loop();
    sendDevices(jsonFinal);
    tempoFinal = millis();
    Serial.println((tempoFinal - tempoInicial));
    jsonRecebido = "";
    jsonFinal = "";
    tempoInicial = 0;
    tempoFinal = 0;
    }
  
}
