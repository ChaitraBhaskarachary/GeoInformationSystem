import os 
from pytz import timezone 
import time as ti 
import os.path 
import datetime 
import subprocess 
import shlex from gpspuller3 
import gpspull 
import pytz 
import shutil 
import glob 

tic=ti.time() 
ss=100000000 

#Acquire image and name file based on date-time 
os.chdir('/media/usb/webcam') 
#acquire image. Image size is 1024 x 768. Camera waits 3 sec before capture to settle exposure. 
os.system('raspistill -o webcam2.jpg -q 90 -w 1024 -h 768 -t 3000 -vf -hf -n') 
path='/media/usb/webcam/webcam2.jpg' 

#stamp on gps fix 
[gpsfix,lat,lon,gpstime]=gpspull() 
print ("pull done") 

# debug to check that gpspull is not hanging 
#stamp on network connection (for time sync info) 
command_line="ping -c 1 www.google.com" 
args=shlex.split(command_line) 
try: 
  subprocess.check_call(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE) 
  s="Internet time-sync: yes" 
except subprocess.CalledProcessError: 
  s="Internet time-sync: no" 

for fname in glob.glob(path): 
  print (fname) 
  t3=os.path.getmtime(fname) #get system time of filename
  tt=ti.localtime(t3) 
  t4=datetime.datetime.fromtimestamp(t3) 
  s1=fname
 #stamp on gps coordinates
 if lat=='nan':
   latstring='Lat: nan'
   lonstring='Lon: nan'
 else:
   latstring='Lat: '+str(lat)
   lonstring='Lon: '+str(lon)
 
 #make big string at bottom
 t4s=str(t4)
 tz=ti.strftime('%Z',ti.gmtime())
 bigstring=t4s+' '+tz+' | '+s+' | '+gpsfix+' | '+latstring+' | '+lonstring
 
 #save image with date filename
 t5=ti.strftime('%Y%m%d%H%M%S',tt)
 imagename=t5+'.jpg'
 d0='/media/usb/webcam/'+imagename
 cmdstring="/usr/bin/convert "+s1+" -pointsize 17 -fill white -annotate +20+760 ‘"+bigstring+"’ "+d0
 os.system(cmdstring)
 
 #Archive current image in date-time folder structure
 year=ti.strftime('%Y',tt)
 month=ti.strftime('%m',tt)
 day=ti.strftime('%d',tt)
 hour=ti.strftime('%H',tt)

 t=pytz.timezone(ti.tzname[1])
 t4aware=t.localize(t4)
 if not gpstime=='nan':
  difft=gpstime-t4aware
  ss=difft.total_seconds()
 
 if ss<120 and gpsfix=='GPS time-sync: yes' and not gpstime=='nan':
  d1='/media/usb/webcam/'+year+'/'+month+'/'+day+'/'+hour+'/'+imagename
 else:
  d1='/media/usb/webcam/unsuretimestamp/'+year+'/'+month+'/'+day+'/'+hour+'/'+imagename
 
 d2=os.path.dirname(d1)
 #if file path does not exist, make it
 if not os.path.exists(d2):
  os.makedirs(d2)
 
 shutil.copyfile(d0,'/var/www/image.jpg') #copy image to webserver directory
 #print d0
 #print d1
 shutil.move(d0,d1) #move file to new date folder

#write metadata text file for webserver
f=open('metadata.txt','w')
f.write(t5+'\n')
f.close()
shutil.move('metadata.txt','/var/www/metadata.txt')

toc=ti.time()
print(toc-tic)
