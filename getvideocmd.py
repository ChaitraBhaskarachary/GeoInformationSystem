#Script 7 acquires h264 format video for a set duration, which is set in the command line
#Script uses the Raspivi function, currently set at frame rate of 10 fps. 
#Script then writes a metadata file with time and position and archives video and metadata file in 
#date based folder structure. Script can be scheduled in cron to run at intervals.


import os
import time as ti
from gpspuller3 import gpspull
import datetime
import subprocess
import shlex
import argparse
import shutil

#manages input from command line, where you input duration of video 
parser=argparse.ArgumentParser(description='this takes video') 
parser.add_argument('-i','--input',help='Input time in sec',required=True) 
arg=parser.parse_args()

print(arg) 
d=arg.input 
print (d)
print (type(d))
d=int(d) 
x=d*1000

os.chdir('/media/usb/webcam/') 
#use raspivid to acquire video at 10 fps 
try: 
  os.system('sudo /etc/init.d/cron stop') 
  ds=str(x) 
  tt0=ti.localtime(ti.time()) 
  t50=ti.strftime('%Y%m%d%H%M%S',tt0) 
  print(t50) 
  a='raspivid -o video.h264 -hf -vf -b 120000000 -fps 10 -t '+ds 
  os.system(a) 
except: 
  print('oops') 
  os.system('sudo /etc/init.d/cron start')
  
  t3=os.path.getmtime('video.h264') 
  tt=ti.localtime(t3) 
  t5=ti.strftime('%Y%m%d%H%M%S',tt) 
  imagename=t5+'.h264' 
  d0='/media/usb/webcam/'+imagename 
  os.rename('video.h264',imagename) 
  
  #Archive current image in date-time folder structure 
  year=ti.strftime('%Y',tt) 
  month=ti.strftime('%m',tt) 
  day=ti.strftime('%d',tt) 
  hour=ti.strftime('%H',tt)
  
  d1='/media/usb/webcam/'+year+'/'+month+'/'+day+'/'+hour+'/'+imagename 
  d2=os.path.dirname(d1)
  
  if not os.path.exists(d2):
    os.makedirs(d2)
  shutil.move(d0,d1)

#write metadata text file
f=open('metadata.txt','w') 

[gpsfix,lat,lon,gpstime]=gpspull() 
latstring='Lat: '+str(lat) 
lonstring='Lon: '+str(lon) 

#stamp on network connection (for time sync info) 
command_line="ping -c 1 www.google.com"
args=shlex.split(command_line) 
try: 
  subprocess.check_call(args,stdout=subprocess. 
  PIPE,stderr=subprocess.PIPE) 
  s="Internet time-sync: yes" 
 except subprocess.CalledProcessError: 
  s="Internet time-sync: no" 
  
 currenttime='Start time of acquisition (HST): '+t50 
 
 xx='Raspberry Pi camera module' 
 f.write(xx+'\n') 
 f.write(currenttime+'\n') 
 f.write(latstring+'\n') 
 f.write(lonstring+'\n') 
 f.write(s+'\n') 
 f.write(gpsfix) 
 
 f.close() 
 os.chdir('/media/usb/webcam/') 
 metaname=t5+'.txt' dx='/media/usb/webcam/'+metaname 
 os.rename('metadata.txt',metaname) 
 
 #Archive metadata in date-time folder structure 
 year=ti.strftime('%Y',tt) 
 month=ti.strftime('%m',tt) 
 day=ti.strftime('%d',tt) 
 hour=ti.strftime('%H',tt) 
 
 d1='/media/usb/webcam/'+year+'/'+month+'/'+day+'/'+hour+'/'+metaname 
 
 d2=os.path.dirname(d1) 
 
 if not os.path.exists(d2): 
  os.makedirs(d2) 
  
 shutil.move(dx,d1)
