#include <ArduinoJson.h>
#include <set>
#include <string>
#include "./functions.h"
#include <ESP8266WiFi.h>

#define PURGETIME 600000
#define MAXDEVICES 60
#define JBUFFER 15+ (MAXDEVICES * 40)
#define disable 0
#define enable  1
#define TopicMQTT "SPI"
#define SENDTIME 30000
#define MINRSSI -99

unsigned int channel = 1;
int clients_known_count_old = 0, aps_known_count_old = 0;

char jsonString[JBUFFER];
int16_t utc = -3; //UTC -3:00 Brazil
StaticJsonBuffer<JBUFFER>  jsonBuffer;
unsigned long sendEntry, deleteEntry;


void purgeDevice() {
  for (int u = 0; u < clients_known_count; u++) {
    if ((millis() - clients_known[u].lastDiscoveredTime) > PURGETIME) {
      for (int i = u; i < clients_known_count; i++) memcpy(&clients_known[i], &clients_known[i + 1], sizeof(clients_known[i])); 
      clients_known_count--;
      break;
    }
  }
  for (int u = 0; u < aps_known_count; u++) {
    if ((millis() - aps_known[u].lastDiscoveredTime) > PURGETIME) {
      for (int i = u; i < aps_known_count; i++) memcpy(&aps_known[i], &aps_known[i + 1], sizeof(aps_known[i]));
      aps_known_count--;
      break;
    }
  }
}


void sendDevices() {
  String deviceMac;
  
  // Setup MQTT
  wifi_promiscuous_enable(disable);
  
  yield();
  // Purge json string
  jsonBuffer.clear();
  JsonObject& root = jsonBuffer.createObject();
  JsonArray& node = root.createNestedArray("NODE");
  JsonArray& mac = root.createNestedArray("MAC");
  JsonArray& rssi = root.createNestedArray("RSSI");
    
  node.add(TopicMQTT);
  
  // add Beacons
  for (int u = 0; u < aps_known_count; u++) {
    deviceMac = formatMac1(aps_known[u].bssid);
    if (aps_known[u].rssi > MINRSSI) {
      mac.add(deviceMac);
      rssi.add(aps_known[u].rssi);
    }
  }

  // Add Clients
  //clientinfo ci;
  for (int u = 0; u < clients_known_count; u++) {
    deviceMac = formatMac1(clients_known[u].station);
    if (clients_known[u].rssi > MINRSSI) {
      mac.add(deviceMac);
      rssi.add(clients_known[u].rssi);
      }
     // clients_known[u] = ci;
  }
  root.printTo(jsonString);
  Serial.println(jsonString);
  strcat(jsonString, "");
  jsonBuffer.clear();
  deviceMac = "";
  clients_known_count_old = 0;
  aps_known_count_old = 0;
  delay(1000);
  wifi_promiscuous_enable(enable);
  sendEntry = millis();
}

boolean scan(){
  channel = 1;
  boolean sendMQTT = false;
  wifi_set_channel(channel);
  while (true) {
    nothing_new++;                          // Array is not finite, check bounds and adjust if required
    if (nothing_new > 200) {                // monitor channel for 200 ms
      nothing_new = 0;
      channel++;
      if (channel == 12) break;             // Only scan channels 1 to 14
      wifi_set_channel(channel);
    }
    delay(1);  // critical processing timeslice for NONOS SDK! No delay(0) yield()

    if (clients_known_count > clients_known_count_old) {
      clients_known_count_old = clients_known_count;
      sendMQTT = true;
    }
    if (aps_known_count > aps_known_count_old) {
      aps_known_count_old = aps_known_count;
      sendMQTT = true;
    }
    if (millis() - sendEntry > SENDTIME) {
      sendEntry = millis();
      sendMQTT = true;
    }
  }
}

void setupSerial(){
  Serial.begin(115200);
}

void setupWifiPromiscuous(){
  wifi_set_opmode(STATION_MODE);            // Promiscuous works only with station mode
  wifi_set_channel(channel);
  wifi_promiscuous_enable(disable);
  wifi_set_promiscuous_rx_cb(promisc_cb);   // Set up promiscuous callback
  wifi_promiscuous_enable(enable);
}
