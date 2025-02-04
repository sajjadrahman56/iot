### **Step-by-Step Explanation of the Code**
 
---

## **1. Including Required Libraries**
```cpp
#include <ESP8266WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"
```
- **ESP8266WiFi.h** → Allows the ESP8266 to connect to WiFi.
- **Adafruit_MQTT.h** & **Adafruit_MQTT_Client.h** → These are used to communicate with **Adafruit IO**, an MQTT broker (a cloud service that sends and receives data).

---

## **2. Defining Variables**
```cpp
#define led1           D1
#define led2           D2
```
- `D1` and `D2` are the **digital pins** on the ESP8266 where the LEDs are connected.
- `#define` is used to **assign names** to these pins for better readability.

### **WiFi Credentials**
```cpp
#define WLAN_SSID       "JayGanesha"             
#define WLAN_PASS       "chandodhar"  
```
- These lines store **WiFi name (SSID)** and **password** so the ESP8266 can connect to the internet.

### **MQTT Server Details**
```cpp
#define AIO_SERVER      "io.adafruit.com" 
#define AIO_SERVERPORT  1883                   
#define AIO_USERNAME    ""    
#define AIO_KEY         ""
```
- **AIO_SERVER** → Adafruit IO’s server for MQTT communication.
- **AIO_SERVERPORT 1883** → The default port for MQTT communication.
- **AIO_USERNAME & AIO_KEY** → The **username and API key** required to connect to Adafruit IO.

---

## **3. Setting Up MQTT Communication**
```cpp
WiFiClient client;
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);
```
- `WiFiClient client;` → Creates an **internet connection**.
- `Adafruit_MQTT_Client mqtt(...);` → Creates an **MQTT connection** between ESP8266 and Adafruit IO.

### **Defining Feeds (Topics)**
```cpp
Adafruit_MQTT_Subscribe Light1 = Adafruit_MQTT_Subscribe(&mqtt, AIO_USERNAME "/feeds/led01"); 
Adafruit_MQTT_Subscribe Light2 = Adafruit_MQTT_Subscribe(&mqtt, AIO_USERNAME "/feeds/led02");
```
- **Light1** and **Light2** are **feeds (topics)** that store LED control data.
- When the ESP8266 **receives a message from these feeds**, it turns LEDs ON or OFF.

---

## **4. Setup Function (Runs Once at Start)**
```cpp
void setup() {
  Serial.begin(115200);
```
- `Serial.begin(115200);` → Starts serial communication for debugging.
  
```cpp
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
```
- `pinMode(led1, OUTPUT);` → Sets **led1** as an **output** pin (so we can turn it ON/OFF).
- `pinMode(led2, OUTPUT);` → Sets **led2** as an output.

### **Connecting to WiFi**
```cpp
  Serial.print("Connecting to ");
  Serial.println(WLAN_SSID);

  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("WiFi connected");
  Serial.println("IP address: "); 
  Serial.println(WiFi.localIP());
```
- This connects the ESP8266 to **WiFi**.
- `WiFi.begin(WLAN_SSID, WLAN_PASS);` → Starts connecting to WiFi.
- `while (WiFi.status() != WL_CONNECTED)` → Keeps checking until WiFi is connected.
- `Serial.print(".");` → Prints dots on the screen while connecting.

### **Subscribing to MQTT Feeds**
```cpp
  mqtt.subscribe(&Light1);
  mqtt.subscribe(&Light2);
```
- This tells the ESP8266 to **listen for messages** from the **Light1 and Light2 feeds**.

---

## **5. Loop Function (Runs Continuously)**
```cpp
void loop() {
  MQTT_connect();
```
- The `loop()` function **runs over and over again**.
- `MQTT_connect();` → Checks if MQTT is connected.

### **Reading Data from MQTT Feeds**
```cpp
  Adafruit_MQTT_Subscribe *subscription;
  while ((subscription = mqtt.readSubscription(20000))) {
```
- `mqtt.readSubscription(20000);` → Checks if a new message has arrived in the last **20 seconds**.

#### **Checking Which Feed Sent Data**
```cpp
    if (subscription == &Light1) {
      Serial.print(F("Got: "));
      Serial.println((char *)Light1.lastread);
      int Light1_State = atoi((char *)Light1.lastread);
      digitalWrite(led1, Light1_State);
    }
```
- If the received message is from **Light1**, it reads the value.
- `atoi((char *)Light1.lastread);` → Converts the received text ("0" or "1") into a number.
- `digitalWrite(led1, Light1_State);` → Turns the LED **ON (1) or OFF (0)**.

Similarly, the same happens for **Light2**:
```cpp
    if (subscription == &Light2) {
      Serial.print(F("Got: "));
      Serial.println((char *)Light2.lastread);
      int Light2_State = atoi((char *)Light2.lastread);
      digitalWrite(led2, Light2_State);
    }
```
---

## **6. Connecting to MQTT Server**
```cpp
void MQTT_connect() {
  int8_t ret;

  if (mqtt.connected()) {
    return;
  }

  Serial.print("Connecting to MQTT... ");
```
- This function **checks if MQTT is connected**.
- If **already connected**, it does nothing.
- Otherwise, it **tries to reconnect**.

### **Retrying the MQTT Connection**
```cpp
  uint8_t retries = 3;
  while ((ret = mqtt.connect()) != 0) {
    Serial.println(mqtt.connectErrorString(ret));
    Serial.println("Retrying MQTT connection in 5 seconds...");
    mqtt.disconnect();
    delay(5000); 
    retries--;
    if (retries == 0) {
      while (1);
    }
  }
  Serial.println("MQTT Connected!");
}
```
- If the MQTT connection fails, it **retries 3 times**.
- If all retries fail, it **stops trying** (the program will not work without an internet connection).

---

## **Final Summary**
### **What This Code Does**
1. **Connects the ESP8266 to WiFi.**
2. **Subscribes to two MQTT feeds** (Light1 and Light2).
3. **Reads messages from the feeds**.
4. **Turns ON/OFF the LEDs** based on the received messages.
5. **Reconnects to MQTT if disconnected**.

---

## **Keywords & Important Terms**
| **Term** | **Meaning** |
|----------|------------|
| `#define` | Creates a name for a value (constant). |
| `WiFi.begin(SSID, PASS)` | Connects ESP8266 to WiFi. |
| `pinMode(PIN, OUTPUT)` | Sets a pin to output mode. |
| `digitalWrite(PIN, HIGH/LOW)` | Turns an LED ON or OFF. |
| `mqtt.subscribe(&Light1)` | Subscribes to MQTT feed. |
| `mqtt.readSubscription()` | Reads data from Adafruit IO. |
| `atoi(value)` | Converts text ("1"/"0") to a number (1/0). |

---

## **How to Explain to Students**
- **Think of MQTT like a messaging app (WhatsApp/Telegram).**
- **Adafruit IO** is like a **group chat** where ESP8266 listens for messages.
- When a message **"Turn on LED1"** is received, it **turns ON** the LED.
- When a message **"Turn off LED1"** is received, it **turns OFF** the LED.
- The ESP8266 is just **waiting for new messages** and responding accordingly.

---
 
