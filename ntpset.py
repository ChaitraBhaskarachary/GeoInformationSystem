#Script5: ntpset.py
#this function tries to ensure the NTP server has the correct time


import os
from setapproxtime2 import setapproxtime
setapproxtime()
os.system(‘sudo service ntp stop’)
os.system(‘sudo ntpd -q’)
os.system(‘sudo service ntp start’)
