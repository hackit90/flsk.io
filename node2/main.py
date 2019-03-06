#ProjectName:               Abschlussarbeit, Objektorientiertes Programmieren
#Autor:                     Kanapathipillai Subakeesan (Subi)
#Projekt Dokumentation:     https://flsk.io
#TTN:                       Europe | 3400 Burgdorf LW-GATEWAY_ID
#ProjectDate:               2019-03-20
#Ordner:                   /lib

#Bibliotheken importieren von /lib
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
#LED leutchtet grün, sofern nicht verbunden mit dem LORA WAN
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
pycom.heartbeat(False)
pycom.rgbled(0x7f7f00)

# ABP Aktivierung aufs TTN (thethingsnetwork)
# Mit Verwendung meiner API KEYS von TTN
dev_addr = struct.unpack(">l", binascii.unhexlify('26011DD8'))[0]
nwk_swkey = binascii.unhexlify('69D2F65B57521C5773A9520335B86760')
app_swkey = binascii.unhexlify('F5F9A4E627B50DE7BD789D654589C4C5')

# Channel Cleaning von nicht verwendeten Channels auf Lora Modul
for i in range(3, 16):
    lora.remove_channel(i)

# Alle Channels auf die gleiche Frequenz stellen
lora.add_channel(0, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)

#LED leuchtet ganz weiss, bis sich etwas connected
pycom.rgbled(0xffffff)

# Verbindung an das nächste LORA WAN Netz mit ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# LORA Socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)
s.setblocking(True)

# cayenneLPP (Low Power Packet) definieren mit einer bytegrösse von max. 100bytes
lpp = cayenneLPP.CayenneLPP(size = 100, sock = s)

####
#### Ab diesem Abschnitt werden in einer endlosen Schlaufe Daten übermittelt, solange die LORAWAN Verbindung steht
####

# Channel Aufbau:
# 1xx = Gyro (Li)
# 2xx = Licht (lt)
# 3xx = Accelerometerdaten (acc)
# 4xx = Temperatur/Feuchtigkeit (si)
# 5xx = Druck (mpp)
# 6xx = Höhenmeter (mp)

pycom.heartbeat(True)
while True:

    # xyz von accelerometer sensor ablesen und senden, wobei die z-Achse mit meinem PySense noch nicht existiert,
    # muss aber zwingend mitgeschickt werden
    xyz = li.acceleration()
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]
    lpp.add_accelerometer(x,y,z, channel = 101)
    print("xyz:",xyz)
    lpp.send(reset_payload = True)

    # lichtsensor inkl. lichtberechnung (multiplikation) zweier Farblichtsensoren.
    # muss dazu zuerst die einzelnen Zahlen im Array - zu INT-format darstellen
    light = lt.light()
    light0 = light[0]
    light1 = light[1]
    lpp.add_luminosity(light0, channel = 201)
    lpp.add_luminosity(light1, channel = 202)
    print("light",light)
    lpp.send(reset_payload = True)

    # Gyroscopdaten auslesen (Grad)
    xg = acc.pitch()
    yg = acc.roll()
    zg = 0
    lpp.add_gyrometer(xg,yg,zg, channel = 301)
    print("gyro",xg,yg,zg)
    lpp.send(reset_payload = True)

    # Barometer / Druckmessung - in Pascal, Umrechnung in Hectopascal muss vorgenommen werden
    druck = mpp.pressure()
    druck = druck/100 #Für Hectopascal
    print("druck",druck)
    lpp.add_barometric_pressure(druck, channel = 501)
    print("druck",druck)
    lpp.send(reset_payload = True)

    # Temperatur des Sensors auslesen in Celsius
    temperatur = si.temperature()
    lpp.add_temperature(temperatur, channel = 401)
    print("temperatur",temperatur)
    lpp.send(reset_payload = True)

    # Höhenmeter des Sensors anhand des Druckes von Pascal umgerechnet
    mum = mp.altitude()
    lpp.add_analog_output(mum, channel = 601)
    print("meteruebermeer",mum)
    lpp.send(reset_payload = True)

    # Feuchtigkeit messen
    humid = si.humidity()
    lpp.add_relative_humidity(humid, channel = 402)
    print("humid",humid)
    lpp.send(reset_payload = True)

    time.sleep(120)
