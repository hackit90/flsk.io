#4TABULARASA HACKIT.IO - FIPY1 LORAGW: b'30aea4FFFE2d6948'
#/dev/tty.usbmodemPy343431
#import os
#os.mkfs('/flash')

"""
HACKIT.IO THINGSNETWORK FIPY1
CONFIG: WIFI_SSID and WIFI_PASS
LORA_FREQUENCY FOR SWITZERLANDE
"""

#from network import WLAN
#import ubinascii
#wl = WLAN()
#ubinascii.hexlify(wl.mac())[:6] + 'FFFE' + ubinascii.hexlify(wl.mac())[6:]

import config
import pycom
import time
from nanogateway import NanoGateway

pycom.heartbeat(False)
pycom.rgbled(0x110000)

if __name__ == '__main__':
    nanogw = NanoGateway(
        id=config.GATEWAY_ID,
        frequency=config.LORA_FREQUENCY,
        datarate=config.LORA_GW_DR,
        ssid=config.WIFI_SSID,
        password=config.WIFI_PASS,
        server=config.SERVER,
        port=config.PORT,
        ntp_server=config.NTP,
        ntp_period=config.NTP_PERIOD_S
        )

    nanogw.start()
    pycom.heartbeat(True)
    nanogw._log('ENTER to enter the REPL')
input()
