#Script 4 reads in NMEA sentences from a serial GPS device plugged into the Raspberry
#Pi. Looks at 30 sentences and takes out GPRMC line, and then reads lat and lon and
#time.
# Matt Patrick
# US Geological Survey - Hawaiian Volcano Observatory
# Mar 20, 2014

import os
import time
import re
import datetime as dt
import pytz

def gpspull():
 print ('pulling GPS time...')
 a=os.listdir(‘/sys/bus/usb-serial/devices’)
 
 #Acquire image and name file based on date-time
 os.chdir(‘/media/usb/webcam’)
 s=’head --lines=30 /dev/’+a[0]+’ > gpsinfo4.txt’
 os.system(s)
 
 isactive=’nan’
 lat=’nan’
 lon=’nan’
 gpstime=’nan’
 
 fh=open(‘gpsinfo4.txt’)
 for line in fh.readlines():
  #print(line[1:6])
  if line[1:6]==’GPRMC’:
    #print(‘yes’)
    s=re.split(‘,’,line)
    isactive=s[2]
    if isactive==’A’:
       slat=s[3]
       slat1=int(float(slat)/100)
       slat2=float(slat)-(slat1*100)
       slat2=slat2/60
       lat=slat1+slat2
       slon=s[5]
       slon1=int(float(slon)/100)
       slon2=float(slon)-(slon1*100)
       slon2=slon2/60
       lon=slon1+slon2
       lat=str(lat)
       lat=float(lat[0:11])
       lon=str(lon)
       lon=float(lon[0:11])
       
       if s[4]==’S’:
        lat=lat*-1
       if s[6]==’W’:
        lon=lon*-1
      
       t1=s[1]
       thour=int(t1[0:2])
       tmin=int(t1[2:4])
       tsec=int(t1[4:6])  
       t2=s[9]
       tday=int(t2[0:2])
       tmonth=int(t2[2:4])
       tyear=int(t2[4:6])+2000
       utc=pytz.UTC
       gpstime=dt.datetime(tyear,tmonth,tday,thour,tmin,tsec,0,utc) 
       
 if isactive==’nan’:
 gpslock=’GPS time-sync: no’
 elif isactive==’V’:
 gpslock=’GPS time-sync: no’
 elif isactive==’A’:
 gpslock=’GPS time-sync: yes’
 fh.close()
 return (gpslock, lat, lon, gpstime)
