from network import WLAN
from mqtt import MQTTClient
import machine
import time

def settimeout(duration):
    pass

wlan = WLAN(mode=WLAN.STA)
wlan.antenna(WLAN.EXT_ANT)
wlan.connect("HAWAIIAN PARADISE", auth=(WLAN.WPA2, "rustichill575"), timeout=5000)

while not wlan.isconnected():
     machine.idle()
print("Connected to Wifi\n")
​
client = MQTTClient("hackitiolopy2", "io.adafruit.com",user="hackit", password="c0ae248ed7ac40a49270bc7ad26e6ce2", port=1883)

client.connect()

client.subscribe(topic="hackit/feeds/raw")
​
while True:
    print("Sending ON")
    client.publish(topic="hackit/feeds/raw", msg="ON")
    time.sleep(1)
    print("Sending OFF")
    client.publish(topic="hackit/feeds/raw", msg="OFF")
    client.check_msg()
​
    # time.sleep(1)
