#include <dummy.h>

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WiFiMulti.h> 
#include <ESP8266mDNS.h>
#include <ESP8266WebServer.h>

ESP8266WiFiMulti wifiMulti;     // For multiple wi-fi configuratiosn
ESP8266WebServer server(80);    // Create a webserver object that listens for HTTP request on port 80

const int RELAY_CONTROL_PIN = 5;



void setup(void){
  delay(1000);
  pinMode(RELAY_CONTROL_PIN, OUTPUT); // working pin
  digitalWrite(RELAY_CONTROL_PIN, 0);
  pinMode(LED_BUILTIN, OUTPUT); // built-in led
  digitalWrite(LED_BUILTIN, HIGH);

  
  Serial.begin(9600);         // Start the Serial communication to send messages to the computer
  delay(10);
  Serial.println('\n');

  wifiMulti.addAP("~^~", "sonik608");   // add Wi-Fi networks you want to connect to
  wifiMulti.addAP("~", "sonik608");

  Serial.println("Connecting ...");
  int i = 0;
  while (wifiMulti.run() != WL_CONNECTED) { // Wait for the Wi-Fi to connect: scan for Wi-Fi networks, and connect to the strongest of the networks above
    delay(250);
    Serial.print('.');
  }
  Serial.println('\n');
  Serial.print("Connected to ");
  Serial.println(WiFi.SSID());               // Tell us what network we're connected to
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());            // Send the IP address of the ESP8266 to the computer

  if (MDNS.begin("esp8266")) {              // Start the mDNS responder for esp8266.local
    Serial.println("mDNS responder started");
  } else {
    Serial.println("Error setting up MDNS responder!");
  }

  server.on("/", HTTP_GET, handleRoot);        // Call the 'handleRoot' function when a client requests URI "/"
  server.on("/command", HTTP_POST, handleRequest); // Call the 'handRequest' function when a POST request is made to URI "/command"
  server.onNotFound(handleNotFound); // When a client requests an unknown URI 

  server.begin(); // Actually start the server
  Serial.println("HTTP server started");
  return;
}

void loop(void){
  server.handleClient(); // Listen for HTTP requests from clients
  return;
}

void handleRoot() {  // When URI / is requested, send a standard web page 
  server.send(200, "text/html", "Wi-fi Remote Control Example");
  return;
}

void handleNotFound(){
  server.send(404, "text/plain", "404: Not found"); // Send HTTP status 404 (Not Found) when there's no handler for the URI in the request
  return;
}

void handleRequest() { // If a POST request is made to URI /command
  // Validate parameters
  if(!server.hasArg("pin") || !server.hasArg("value") || server.arg("pin") == NULL || server.arg("value") == NULL) { 
    server.send(400, "text/plain", "400: Invalid Request");         // The request is invalid, so send HTTP status 400
    return;
  }
  
  // Get the parameters: pin and value
  String temp = "";
  temp = server.arg("pin"); 
  int pin = temp.toInt();
  temp = server.arg("value"); 
  int value = temp.toInt();

  Serial.println(pin);
  Serial.println(value);
  if (pin >= 0 && pin < 17 && value >= 0 && value <= 100) {
    switch (pin) {
      case 0:
        analogWrite(pin, value);
        break;
      case 2: // avoid builtin led pin
        digitalWrite(RELAY_CONTROL_PIN, value);
        break;
      default:
        digitalWrite(pin, value);
        break;
    }
  }
  
  server.send(200, "text/html", "Wi-fi Remote Control Example");
  return;
}
