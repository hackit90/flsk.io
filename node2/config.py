"""
#ProjectName:               Abschlussarbeit, Objektorientiertes Programmieren
#Autor:                     Kanapathipillai Subakeesan (Subi)
#Projekt Dokumentation:     https://flsk.io
#TTN:                       Europe | 3400 Burgdorf LW-GATEWAY_ID
#Ordner:                   /lib
#File:                     main.py

#Bibliotheken importieren von /lib

#####
#Dieser Konfig-Teil dient vielleicht mal der Zukunft, falls man in einem Umfeld ist, wo man immer das WLAN-Modul
#statt LORA verwenden möchte
####

import machine
import ubinascii

WIFI_MAC = ubinascii.hexlify(machine.unique_id()).upper()

# GW-ID wird anhand der ersten 3 bytes der MAC Adresse + 'FFFE' + die letzten 3 bytes der MAC definiert
GATEWAY_ID = WIFI_MAC[:6] + "FFFE" + WIFI_MAC[6:12]

SERVER = 'router.eu.thethings.network'
PORT = 1700

NTP = "pool.ntp.org"
NTP_PERIOD_S = 3600

# for EU868
LORA_FREQUENCY = 868100000
LORA_GW_DR = "SF7BW125" # DR_5
LORA_NODE_DR = 5
