import machine
from network import WLAN
wlan = WLAN() # get current object, without changing the mode

if machine.reset_cause() != machine.SOFT_RESET:
    wlan.init(mode=WLAN.STA)
    # configuration below MUST match your home router settings!!
    wlan.ifconfig(config=('10.11.12.248', '255.255.255.0', '10.11.12.1', '8.8.8.8'))

if not wlan.isconnected():
    # change the line below to match your network ssid, security and password
    wlan.connect('NextLevel-04', auth=(WLAN.WPA2, 'CiscoRul3s'), timeout=5000)
    while not wlan.isconnected():
        machine.idle() # save power while waiting