# boot.py -- run on boot-up
from network import LoRa, WLAN
import machine
import socket
import time
import pycom
import math
import utime
from dth import DTH
from mqtt import MQTTClient

MQTT = False

wlan = WLAN() # get current object, without changing the mode

if machine.reset_cause() != machine.SOFT_RESET:
    wlan.init(mode=WLAN.STA)
    wlan.ifconfig(config=('10.11.12.246', '255.255.255.0', '10.11.12.1', '8.8.8.8'))

if not wlan.isconnected():
    # change the line below to match your network ssid, security and password
    wlan.connect('NextLevel-04', auth=(WLAN.WPA2, 'CiscoRul3s'), timeout=5000)
    while not wlan.isconnected():
        machine.idle() # save power while waiting

print('Wireless network connected!')
def settimeout(duration): 
    pass

# initialise LoRa in LORA mode
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
# more params can also be given, like frequency, tx power and spreading factor
lora = LoRa(mode=LoRa.LORA, region=LoRa.AU915)
# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

if MQTT:
    client = MQTTClient("demo", "10.11.12.120", port=1883)
    client.settimeout = settimeout
    client.connect()

th = DTH('P3', 1)
time.sleep(2)
last_temp = 0
last_hum = 0
while True:
    result = th.read()
    if result.is_valid():
        ct = utime.ticks_ms()
        s1 = 'Temp: {:3.2f}'.format(result.temperature/1.0)
        s2 = 'Hum: {:3.2f}'.format(result.humidity/1.0)
        s3 = 'Count: {}'.format(ct)
        print(s1)
        print(s2)
        print(s3)
        s.setblocking(True)
        s.send(s1 + '\n' + s2 + '\n' + s3)
        s.setblocking(False)
        temp = s1.split(':')[1].strip()
        hum = s2.split(':')[1].strip()
        if abs(float(temp) - float(last_temp)) > 0.1:
            if MQTT: client.publish("/temp", temp)
            print(temp)
        if abs(float(hum) - float(last_hum)) > 0.1:
            if MQTT: client.publish("/hum", hum)
            print(hum)
        last_temp = temp
        last_hum = hum
    time.sleep(2)