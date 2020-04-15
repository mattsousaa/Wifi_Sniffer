
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <set>
#include <string>
#include "./scan.h"


void setup() {
  setupSerial();
  setupWifiPromiscuous();
}

void loop() {
  boolean aux = scan();
  purgeDevice();
  if (aux) {
    //   showDevices();
    sendDevices();
  }

}
