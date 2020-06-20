#Script6: setapproximate2.py 
#this function uses the RTC time on the Ultimate GPS module (gps lock or not) 
#to roughly set NTP, to ensure it is close enough that NTP can do self correction

import os
import time
import datetime as dt
from gpspuller3 import gpspull
from pytz import timezone

def setapproxtime():
 [gpsfix,lat,lon,gpstime]=gpspull()
 print(gpstime)
 
 t=gpstime.astimezone(timezone('UTC'))
 
 gpstime=t 
 year=str(gpstime.year) 
 month=str(gpstime.month)
 day=str(gpstime.day)
 hour=str(gpstime.hour)
 mint=str(gpstime.minute)
 sec=str(gpstime.second)
 
 s1=year+'-'+month+'-'+day 
 s1b='sudo date --set="'+s1 
 s2=hour+':'+mint+':'+sec 
 s3=s1b+' '+s2+'"' 
 
 os.system(s3)
