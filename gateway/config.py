"""
HACKIT.IO THINGSNETWORK FIPY1
CONFIG: WIFI_SSID and WIFI_PASS
LORA_FREQUENCY FOR SWITZERLANDE
"""
import machine
import ubinascii

WIFI_MAC = ubinascii.hexlify(machine.unique_id()).upper()
# Set  the Gateway ID to be the first 3 bytes of MAC address + 'FFFE' + last 3 bytes of MAC address
GATEWAY_ID = WIFI_MAC[:6] + "FFFE" + WIFI_MAC[6:12]

SERVER = 'router.eu.thethings.network'
PORT = 1700

NTP = "pool.ntp.org"
NTP_PERIOD_S = 3600

WIFI_SSID = 'HAWAIIAN PARADISE'
WIFI_PASS = 'rustichill575'

# for EU868 and Switzerlande
LORA_FREQUENCY = 868100000
LORA_GW_DR = "SF7BW125" # DR_5
LORA_NODE_DR = 5
