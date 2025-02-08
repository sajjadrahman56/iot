import network
import time
import machine
from umqtt.simple import MQTTClient

# WiFi Credentials
WIFI_SSID = "JayGanesha"
WIFI_PASS = "chandodhar"

# Adafruit IO Credentials
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USERNAME = ""  # Add your username
AIO_KEY = ""  # Add your API Key

# Define LED pins
led1 = machine.Pin(5, machine.Pin.OUT)  # D1 (GPIO5)
led2 = machine.Pin(4, machine.Pin.OUT)  # D2 (GPIO4)

# Connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Connecting to WiFi: {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(0.5)
            print(".", end="")
    print("\nWiFi connected! IP:", wlan.ifconfig()[0])

# MQTT Callback Function (Handles Incoming Messages)
def sub_cb(topic, msg):
    print(f"Received: {topic.decode()} -> {msg.decode()}")
    
    if topic == bytes(f"{AIO_USERNAME}/feeds/led01", "utf-8"):
        led1.value(1 if msg == b'1' else 0)  # Turn LED1 ON/OFF
    elif topic == bytes(f"{AIO_USERNAME}/feeds/led02", "utf-8"):
        led2.value(1 if msg == b'1' else 0)  # Turn LED2 ON/OFF

# Connect to MQTT Server
def connect_mqtt():
    client = MQTTClient("ESP8266", AIO_SERVER, AIO_PORT, AIO_USERNAME, AIO_KEY)
    client.set_callback(sub_cb)
    client.connect()
    print("Connected to MQTT Broker!")
    
    # Subscribe to feeds
    client.subscribe(f"{AIO_USERNAME}/feeds/led01")
    client.subscribe(f"{AIO_USERNAME}/feeds/led02")
    return client

# Main Loop
def main():
    connect_wifi()
    client = connect_mqtt()

    while True:
        try:
            client.check_msg()  # Check for new MQTT messages
            time.sleep(1)
        except Exception as e:
            print("Error:", e)
            time.sleep(5)
            machine.reset()  # Restart ESP8266 on failure

# Run the program
main()
