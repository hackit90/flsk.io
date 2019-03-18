"""
#ProjectName:               Abschlussarbeit, Objektorientiertes Programmieren
#Autor:                     Kanapathipillai Subakeesan (Subi)
#Projekt Dokumentation:     https://flsk.io
#TTN:                       Europe | 3400 Burgdorf LW-GATEWAY_ID
#ProjectDate:               2019-03-20
#Ordner:                   /lib
#File:                     main.py

#Bibliotheken importieren von /lib
"""

#Notwendige Libraries des Boards und Timeservers laden
import pycom
import time
from nanogateway import NanoGateway

# LED-STATUS: Auf rot stellen, bis die Verbindung aufgebaut ist
pycom.heartbeat(False)
pycom.rgbled(0x110000)

# LoRa NanoGateway Informationen in die Variable nanogw laden
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

# LoRa NanoGateway mit den eingelesenen Informationen starten
    nanogw.start()
    # LED-STATUS: LoRaWAN ist ready, auf weiss Stufe 3 stellen
    pycom.rgbled(0x333333)
    time.sleep(5)

    # LED-STATUS: Auf Heartbeat Mode umstellen, damit Strom gespart wird
    pycom.heartbeat(True)
    nanogw._log('ENTER')
input()
