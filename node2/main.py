import time
import machine
import pycom

from LIS2HH12 import LIS2HH12
from pytrack import Pytrack
#pysense sensor stuff
from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

py = Pysense()
mp = MPL3115A2(py,mode=ALTITUDE) # ALTITUDE IN METER
mpp = MPL3115A2(py,mode=PRESSURE) # PRESSURE IN PASCAL

si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)

py = Pytrack()
acc = LIS2HH12()

#pitch/accelerometer:
while True:
    pitch = acc.pitch()
    roll = acc.roll()
    print('{},{}'.format(pitch,roll))
time.sleep_ms(100)


#str(lt.ligt())
#str(mp.PRESSURE())
#str(mp.altitude())
