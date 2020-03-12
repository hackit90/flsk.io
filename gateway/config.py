"""
#ProjectName:               Abschlussarbeit, Objektorientiertes Programmieren
#Autor:                     Kanapathipillai Subakeesan (Subi)
#Projekt Dokumentation:     https://flsk.io
#TTN:                       Europe | 3400 Burgdorf LW-GATEWAY_ID
#Ordner:                   /lib
#File:                     main.py
"""

import machine
import ubinascii

WIFI_MAC = ubinascii.hexlify(machine.unique_id()).upper()
GATEWAY_ID = WIFI_MAC[:6] + "FFFE" + WIFI_MAC[6:12]

SERVER = 'router.eu.thethings.network'
PORT = 1700

NTP = "pool.ntp.org"
NTP_PERIOD_S = 3600

WIFI_SSID = ''
WIFI_PASS = ''

# for EU868 and Switzerlande
LORA_FREQUENCY = 868100000
LORA_GW_DR = "SF7BW125" # DR_5
LORA_NODE_DR = 5
