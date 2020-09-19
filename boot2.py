# boot.py -- run on boot-up
from network import LoRa
from machine import Pin, rng
import socket
import time
import pycom
from dht import DTH

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

th = DTH('P3', 1)
time.sleep(2)
count = 0
while True:
    count += 10
    if count >= 32000:
        count = 0
    result = th.read()
    if result.is_valid():
        s1 = 'Temp: {:3.2f}'.format(result.temperature/1.0)
        s2 = 'Hum: {:3.2f}'.format(result.humidity/1.0)
        s3 = 'Count: {}'.format(count)
        print(s1)
        print(s2)
        print(s3)
        s.setblocking(True)
        s.send(s1 + '\n' + s2 + '\n' + s3)
        s.setblocking(False)
    # time.sleep(rng() & 0x0F)
    time.sleep(2)