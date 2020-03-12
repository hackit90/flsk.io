"""
#ProjectName:               Abschlussarbeit, Objektorientiertes Programmieren
#Autor:                     Kanapathipillai Subakeesan (Subi)
#Projekt Dokumentation:     https://flsk.io
#TTN:                       Europe | 3400 Burgdorf LW-GATEWAY_ID
#Ordner:                   /lib
#File:                     main.py

#Bibliotheken importieren von /lib
"""

import time
from network import LoRa
import socket
import cayenneLPP
import binascii
import struct
import time
import config
import pycom
import ustruct
import ubinascii

#Sensorelemente importieren von /lib
from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
from CayenneLPP import CayenneLPP

#Einfache Aliases für Sensoren von PySense
acc = LIS2HH12() #Accelerometerdaten x,y,z
py = Pysense() #Alle Pysense Sensoren
mp = MPL3115A2(py,mode=ALTITUDE) #Höhenmeter transformiert mit Druck in Pascal
mpp = MPL3115A2(py,mode=PRESSURE) #Druck in Pascal
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)

#LORA WAN Mode Europa = LoRa.EU868
#LED-STATUS1:INITIALISIERE LORA leuchtet gelb auf voller Stufe, sofern nicht verbunden mit dem LORA WAN
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
pycom.heartbeat(False)
pycom.rgbled(0x7f7f00) # yellow

# Verwendung meiner API KEYS von TTN für den Aufbau von OTA
dev_eui = binascii.unhexlify('30AEA4FFFE786398')
app_eui = binascii.unhexlify('70B3D57ED0012CF5')
app_key = binascii.unhexlify('5F01C38CA544DA99E7893CFFB6F9E071')

# Alle Channels auf die gleiche Frequenz stellen
lora.add_channel(0, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)

# LED-STATUS2:FREQUENZBÄNDER BEREIT, leuchtet weiss, auf Stufe2
pycom.rgbled(0x222222)

# Verbindung an das nächste LORA WAN Netz mit OTA
# OTA Aktivierung aufs TTN (thethingsnetwork), OTA = OVER THE AIR AUTHENTICATION
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=config.LORA_NODE_DR)

# Solange sich die Node noch nicht über OTA aktiviert hat:
# STATUS-LED:Lora!=verbunden | Orange
led_status = 1
while not lora.has_joined():
    pycom.rgbled(0x333000)
    time.sleep(2.5)
    print("OTA Aktivierung in Prozess...")

# Channel Cleaning von nicht verwendeten Channels auf dem Lora Modul
for i in range(3, 16):
    lora.remove_channel(i)

# LORA Socket aufsetzen
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# LORA Datenrate auf dem lib Teil config entnehmen
s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)
s.setblocking(False)

# LED-STATUS:LORA-Verbindung steht geht auf Herzschlagmodus (braucht weniger Strom)
time.sleep(5.0)
if led_status == 1:
    pycom.heartbeat(True)
else:
    print("ein Fehler liegt in der LED-Statusanzeige vor")

####
#### Ab diesem Abschnitt werden in einer endlosen Schlaufe Daten übermittelt, solange die LORAWAN Verbindung steht
####

# cayenneLPP (Low Power Packet) definieren mit einer bytegrösse von max. 100bytes
lpp = cayenneLPP.CayenneLPP(size = 100, sock = s)

# Channel Aufbau:
# 1xx = Gyro (Li)
# 2xx = Licht (lt)
# 3xx = Accelerometerdaten (acc)
# 4xx = Temperatur/Feuchtigkeit (si)
# 5xx = Druck (mpp)
# 6xx = Höhenmeter (mp)

# Während die Verbindung mit Lora besteht, führe folgende WHILE - Schlaufe auslesen
# Nach einer Wartezeit von 30 Sekunden, werden neue Sensordaten verschickt
while lora.has_joined():
    print("joined")

    # xyz von accelerometer sensor ablesen und senden, wobei die z-Achse mit meinem PySense noch nicht existiert,
    # muss aber zwingend mitgeschickt werden
    xyz = li.acceleration()
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]
    lpp.add_accelerometer(x,y,z)
    print("xyz:",xyz)
    lpp.send(reset_payload = True)
    time.sleep(2)

    # lichtsensor inkl. lichtberechnung (multiplikation) zweier Farblichtsensoren.
    # muss dazu zuerst die einzelnen Zahlen im Array - zu INT-format darstellen
    light = lt.light()
    light0 = light[0]
    light1 = light[1]
    lpp.add_luminosity(light0)
    lpp.add_luminosity(light1, channel = 22)
    print("light",light)
    lpp.send(reset_payload = True)
    time.sleep(2)

    # Gyroscopdaten auslesen (Grad)
    xg = acc.pitch()
    yg = acc.roll()
    zg = 0
    lpp.add_gyrometer(xg,yg,zg)
    print("gyro",xg,yg,zg)
    lpp.send(reset_payload = True)
    time.sleep(2)

    # Barometer / Druckmessung - in Pascal, Umrechnung in Hectopascal muss vorgenommen werden
    mpp = MPL3115A2(py,mode=PRESSURE)
    druck = mpp.pressure()
    druck = round(druck/100) #Für Hectopascal
    print("druck",druck)
    lpp.add_barometric_pressure(druck)
    print("druck",druck)
    lpp.send(reset_payload = True)
    time.sleep(2)

    # Temperatur des Sensors auslesen in Celsius
    temperatur = si.temperature()
    lpp.add_temperature(temperatur)
    temperatur = round(temperatur,2)
    print("temperatur",temperatur)
    lpp.send(reset_payload = True)
    time.sleep(2)

    # Höhenmeter des Sensors anhand des Druckes von Pascal umgerechnet
    mp = MPL3115A2(py,mode=ALTITUDE)
    mum = mp.altitude()
    mum = round(mum,2)
    lpp.add_barometric_pressure(mum, channel = 61)
    print("meteruebermeer in km",mum)
    lpp.send(reset_payload = True)
    time.sleep(2)

    # Feuchtigkeit messen
    humid = si.humidity()
    humid = round(humid,2)
    lpp.add_relative_humidity(humid)
    print("humid",humid)
    lpp.send(reset_payload = True)
    time.sleep(2)

    # GPS Daten
    lpp.add_gps(47.353444, 7.904001, 0)
    print("gps statisch")
    lpp.send(reset_payload = True)
    time.sleep(2)

    time.sleep(30)
